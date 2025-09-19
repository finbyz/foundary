# Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe.model.mapper import get_mapped_doc

class ToolRequest(Document):
	pass



@frappe.whitelist()
def make_tool_movement(source_name, target_doc=None):
    def set_missing_values(source, target):
      
        if source.purpose == "Transfer":
            target.tool_movement_type = "Tool Transfer"
        else:
            target.tool_movement_type = "Tool Receipt"
        # map warehouses if present on parent
        target.source_tool_warehouse = source.source_tool_warehouse
        target.target_tool_warehouse = source.target_tool_warehouse

    doc = get_mapped_doc(
        "Tool Request",
        source_name,
        {
            "Tool Request": {
                "doctype": "Tool Movement"
            },
            "Tool Request Details": {
                "doctype": "Tool Movement Details",
                "field_map": {
                    "tool_name": "tool_code",
                   
                    "source_tool_warehouse": "source_warehouse",
                    "target_tool_warehouse": "target_warehouse",
                }
            }
        },
        target_doc,
        set_missing_values
    )

    return doc
