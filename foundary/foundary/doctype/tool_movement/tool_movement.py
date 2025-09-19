# Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, nowtime


class ToolMovement(Document):
	def validate(self):
		# if self.tool_movement_type == "Tool Receipt":
		# 	return

		if self.tool_movement_type == "Tool Transfer":
			for d in self.tool_movement_details:
				if not d.source_warehouse or not d.target_warehouse:
					frappe.throw(f"Row #{d.idx}: Source Warehouse and Target Warehouse is mandatory for Tool Transfer")
		elif self.tool_movement_type == "Tool Receipt":
			for d in self.tool_movement_details:
				if not d.target_warehouse:
					frappe.throw(f"Row #{d.idx}: Target Warehouse is mandatory for Tool Receipt")

		
		for row in self.tool_movement_details:
			if not row.tool_code:
				continue
			if self.tool_movement_type == "Tool Receipt":
				continue
			tool = frappe.get_doc("Tool", row.tool_code)
			default_wh = tool.default_tool_warehouse

			
			last_movement = frappe.db.sql("""
				SELECT 
					tmd.source_warehouse, 
					tmd.target_warehouse, 
					tm.name as parent
				FROM 
					`tabTool Movement Details` tmd
				INNER JOIN 
					`tabTool Movement` tm
				ON 
					tmd.parent = tm.name
				WHERE 
					tmd.tool_code = %s
					AND tm.docstatus = 1   --  Only submitted parent docs
				ORDER BY 
					tmd.creation DESC
				LIMIT 1
			""", row.tool_code, as_dict=True)

			if not last_movement:
				
				if row.source_warehouse != default_wh:
					frappe.throw(
						f"First movement of Tool {row.tool_code} must start from its Default Warehouse {default_wh}"
					)
				continue

			
			last_wh = last_movement[0].target_warehouse

			if last_wh == default_wh:
				# Tool is in default → next movement must start from default
				if row.source_warehouse != default_wh:
					frappe.throw(
						f"Tool {row.tool_code} is currently in {default_wh}, so Source must be {default_wh}"
					)
			else:
				# Tool is outside default → must return to default
				if row.target_warehouse != default_wh:
					frappe.throw(
						f"Tool {row.tool_code} is currently in {last_wh}, so it must move back to Default Warehouse {default_wh}"
					)

		
	def on_submit(self):
		
		if hasattr(self, "status"):
			self.db_set("status", "Submitted")

		for row in self.tool_movement_details:
			tle = frappe.new_doc("Tool Ledger Entry")
			tle.voucher_type = "Tool Movement"
			tle.voucher_no = self.name
			tle.company = self.company

			tle.posting_date = self.date
			tle.posting_time = self.time

			tle.tool_code = row.tool_code
			tle.source_tool_warehouse = row.source_warehouse
			tle.target_tool_warehouse = row.target_warehouse
			

			tle.insert()

	def on_cancel(self):
		if hasattr(self, "status"):
			self.db_set("status", "Cancelled")
		tle_entries = frappe.get_all(
			"Tool Ledger Entry",
			filters={"voucher_type": "Tool Movement",
			"voucher_no": self.name
			},
			fields=["name"]
		)
		if tle_entries:
			for tle in tle_entries:
				tle_doc = frappe.get_doc("Tool Ledger Entry", tle.name)
				tle_doc.is_cancelled = 1
				tle_doc.save()

		for row in self.tool_movement_details:
			tle = frappe.new_doc("Tool Ledger Entry")
			tool = frappe.get_doc("Tool", row.tool_code)
			tle.voucher_type = "Tool Movement"
			tle.voucher_no = self.name
			tle.company = self.company

			tle.posting_date = self.date
			tle.posting_time = self.time

			tle.tool_code = row.tool_code
			tle.source_tool_warehouse = row.target_warehouse
			tle.target_tool_warehouse = tool.default_tool_warehouse
			
			tle.insert()


				

