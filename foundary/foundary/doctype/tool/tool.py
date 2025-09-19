# Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Tool(Document):
    pass
	


@frappe.whitelist()
def get_latest_tool_movement(tool_code):
	# First get latest movement item row for this tool
	latest_item = frappe.db.sql("""
		SELECT tmi.parent
		FROM `tabTool Movement Details` tmi
		JOIN `tabTool Movement` tm ON tm.name = tmi.parent
		WHERE tmi.tool_code = %s
		AND tm.docstatus = 1   -- only submitted
		ORDER BY tm.creation DESC
		LIMIT 1
	""", (tool_code,), as_dict=True)

	if latest_item:
		# fetch full parent doc
		parent_doc = frappe.get_doc("Tool Movement", latest_item[0].parent)
		return {
			"name": parent_doc.name,
			"doc": parent_doc.as_dict(),

		}
	return {}
