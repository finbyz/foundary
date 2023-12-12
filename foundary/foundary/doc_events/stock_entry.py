import json
from collections import defaultdict

import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.query_builder.functions import Sum
from frappe.utils import (
	cint,
	comma_or,
	cstr,
	flt,
	format_time,
	formatdate,
	getdate,
	month_diff,
	nowdate,
)

import erpnext
from erpnext.accounts.general_ledger import process_gl_map
from erpnext.controllers.taxes_and_totals import init_landed_taxes_and_totals
from erpnext.manufacturing.doctype.bom.bom import add_additional_cost, validate_bom_no
from erpnext.setup.doctype.brand.brand import get_brand_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.stock.doctype.batch.batch import get_batch_no, get_batch_qty, set_batch_nos
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.stock.doctype.serial_no.serial_no import (
	get_serial_nos,
	update_serial_nos_after_submit,
)
from erpnext.stock.doctype.stock_reconciliation.stock_reconciliation import (
	OpeningEntryAccountError,
)
from erpnext.stock.get_item_details import (
	get_bin_details,
	get_conversion_factor,
	get_default_cost_center,
	get_reserved_qty_for_so,
)
from erpnext.stock.stock_ledger import NegativeStockError, get_previous_sle, get_valuation_rate
from erpnext.stock.utils import get_bin, get_incoming_rate


class FinishedGoodError(frappe.ValidationError):
	pass


class IncorrectValuationRateError(frappe.ValidationError):
	pass


class DuplicateEntryForWorkOrderError(frappe.ValidationError):
	pass


class OperationsNotCompleteError(frappe.ValidationError):
	pass


class MaxSampleAlreadyRetainedError(frappe.ValidationError):
	pass


from erpnext.controllers.stock_controller import StockController
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry

form_grid_templates = {"items": "templates/form_grid/stock_entry_grid.html"}

class CustomStockEntry(StockEntry):
	def check_if_operations_completed(self):
			"""Check if Time Sheets are completed against before manufacturing to capture operating costs."""
			prod_order = frappe.get_doc("Work Order", self.work_order)
			allowance_percentage = flt(
				frappe.db.get_single_value("Manufacturing Settings", "overproduction_percentage_for_work_order")
			)
			for d in prod_order.get("operations"):
				total_completed_qty = flt(self.fg_completed_qty) + flt(prod_order.produced_qty)
				completed_qty = (
					d.completed_qty + d.process_loss_qty + (allowance_percentage / 100 * d.completed_qty)
				)
				prev_completed_qty = d.completed_qty
				if (prev_completed_qty == 0 and total_completed_qty > flt(completed_qty)) \
					or (prev_completed_qty > 0 and prev_completed_qty > flt(completed_qty)):
					job_card = frappe.db.get_value("Job Card", {"operation_id": d.name}, "name")
					if not job_card:
						frappe.throw(
							_("Work Order {0}: Job Card not found for the operation {1}").format(
								self.work_order, d.operation
							)
						)

					work_order_link = frappe.utils.get_link_to_form("Work Order", self.work_order)
					job_card_link = frappe.utils.get_link_to_form("Job Card", job_card)
					frappe.throw(
						_(
							"Row #{0}: Operation {1} is not completed for {2} qty of finished goods in Work Order {3}. Please update operation status via Job Card {4}."
						).format(
							d.idx,
							frappe.bold(d.operation),
							frappe.bold(total_completed_qty),
							work_order_link,
							job_card_link,
						),
						OperationsNotCompleteError,
					)


	def set_process_loss_qty(self):
			if self.purpose not in ("Manufacture", "Repack"):
				return

			precision = self.precision("process_loss_qty")
			if self.work_order:
				data = frappe.get_all(
					"Work Order Operation",
					filters={"parent": self.work_order},
					fields=["sum(process_loss_qty) as process_loss_qty"],
				)

				finish_data = frappe.get_all(
					"Stock Entry",
					filters={"purpose": "Manufacture", "work_order": self.work_order, "docstatus": 1},
					fields=["sum(process_loss_qty) as process_loss_qty"],
				)

				if data and data[0].process_loss_qty is not None:
					process_loss_qty = flt(data[0].process_loss_qty) - flt(finish_data[0].process_loss_qty)
					if flt(self.process_loss_qty, precision) != flt(process_loss_qty, precision):
						self.process_loss_qty = flt(process_loss_qty, precision)

						frappe.msgprint(
							_("The Process Loss Qty has reset as per job cards Process Loss Qty"), alert=True
						)

			if not self.process_loss_percentage and not self.process_loss_qty:
				self.process_loss_percentage = frappe.get_cached_value(
					"BOM", self.bom_no, "process_loss_percentage"
				)

			if self.process_loss_percentage and not self.process_loss_qty:
				self.process_loss_qty = flt(
					(flt(self.fg_completed_qty) * flt(self.process_loss_percentage)) / 100
				)
			elif self.process_loss_qty and not self.process_loss_percentage:
				self.process_loss_percentage = flt(
					(flt(self.process_loss_qty) / flt(self.fg_completed_qty)) * 100
				)

	def get_scrap_items_from_job_card(self):
			if not self.pro_doc:
				self.set_work_order_details()

			if not self.pro_doc.operations:
				return []

			job_card = frappe.qb.DocType("Job Card")
			job_card_scrap_item = frappe.qb.DocType("Job Card Scrap Item")

			scrap_items = (
				frappe.qb.from_(job_card)
				.select(
					Sum(job_card_scrap_item.stock_qty).as_("stock_qty"),
					job_card_scrap_item.item_code,
					job_card_scrap_item.item_name,
					job_card_scrap_item.description,
					job_card_scrap_item.stock_uom,
				)
				.join(job_card_scrap_item)
				.on(job_card_scrap_item.parent == job_card.name)
				.where(
					(job_card_scrap_item.item_code.isnotnull())
					& (job_card.work_order == self.work_order)
					& (job_card.docstatus == 1)
				)
				.groupby(job_card_scrap_item.item_code)
			).run(as_dict=1)

			pending_qty = flt(self.get_completed_job_card_qty()) - flt(self.pro_doc.produced_qty)

			used_scrap_items = self.get_used_scrap_items()
			for row in scrap_items:
				row.stock_qty -= flt(used_scrap_items.get(row.item_code))
				# row.stock_qty = (row.stock_qty) * flt(self.fg_completed_qty) / flt(pending_qty)

				if used_scrap_items.get(row.item_code):
					used_scrap_items[row.item_code] -= row.stock_qty

				if cint(frappe.get_cached_value("UOM", row.stock_uom, "must_be_whole_number")):
					row.stock_qty = frappe.utils.ceil(row.stock_qty)

			return scrap_items
	
	def get_basic_rate_for_manufactured_item(self, finished_item_qty, outgoing_items_cost=0) -> float:
		scrap_items_cost = sum([flt(d.basic_amount) for d in self.get("items") if d.is_scrap_item])

		# Get raw materials cost from BOM if multiple material consumption entries
		if not outgoing_items_cost and frappe.db.get_single_value(
			"Manufacturing Settings", "material_consumption", cache=True
		):
			bom_items = self.get_bom_raw_materials(finished_item_qty)
			outgoing_items_cost = sum([flt(row.qty) * flt(row.rate) for row in bom_items.values()])
		if finished_item_qty == 0:
			frappe.throw("Please Completed the further Operations.")
		return flt((outgoing_items_cost - scrap_items_cost) / finished_item_qty)

