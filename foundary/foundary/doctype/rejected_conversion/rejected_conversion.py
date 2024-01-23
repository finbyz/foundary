# Copyright (c) 2024, Finbyz Tech PVT LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_url_to_form


class RejectedConversion(Document):
	@frappe.whitelist()
	def get_rejected_items(self):
		company = frappe.get_doc(
			"Company",
			self.company,
		)

		if not self.scrap_rejected_warehouse:
			frappe.throw(
				f"Please set Scrap Rejected Warehouse in Company {self.company}."
			)

		if not self.scrap_target_warehouse:
			frappe.throw(
				f"Please set Scrap Target Warehouse in Company {self.company}."
			)

		if not self.scrap_item:
			frappe.throw(f"Please set Scrap Item in Company {self.company}.")

		return frappe.db.sql(
			f"""
				SELECT
					b.actual_qty as qty, b.item_code, i.item_name
				FROM `tabBin` as b JOIN `tabItem` as i on i.name = b.item_code
				WHERE b.warehouse = '{self.scrap_rejected_warehouse}' AND b.actual_qty > 0 AND b.valuation_rate > 0
			""",
			as_dict=True,
		)

	def validate(self):
		self.repack_stock_entry()
		
		self.company = None
		self.item = []

	def repack_stock_entry(self):
		branch = ""
		if frappe.db.exists("Accounting Dimension", "Branch"):
			ad_doc = frappe.get_doc("Accounting Dimension", "Branch")

			for dd in ad_doc.dimension_defaults:
				if dd.company == self.company:
					branch = dd.default_dimension
					break

		for row in self.item:

			weight_per_unit = frappe.db.get_value(
				"Item", row.item_code, "weight_per_unit"
			)

			if not weight_per_unit:
				continue

			se_doc = frappe.new_doc("Stock Entry")
			se_doc.naming_series = f"A{se_doc.naming_series}"
			se_doc.company = self.company
			se_doc.stock_entry_type = "Repack"
			se_doc.purpose = "Repack"
			se_doc.branch = branch



			se_doc.append(
				"items",
				{
					"s_warehouse": self.scrap_rejected_warehouse,
					"item_code": row.item_code,
					"qty": row.qty,
				},
			)

			se_doc.append(
				"items",
				{
					"t_warehouse": self.scrap_target_warehouse,
					"item_code": self.scrap_item,
					"qty": int(row.qty) * weight_per_unit,
				},
			)

			se_doc.flags.ignore_permissions = True
			se_doc.save()
			se_doc.submit()
		
			item_url = f"<a href='{get_url_to_form('Item', row.item_code)}'>{row.item_code}</a>"
			stock_entry_url = f"<a href='{get_url_to_form('Stock Entry', se_doc.name)}'>{se_doc.name}</a>"
			
			frappe.msgprint(f"Stock Entry for Item {frappe.bold(item_url)} has been created {frappe.bold(stock_entry_url)}")
