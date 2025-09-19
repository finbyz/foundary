# # Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
# # For license information, please see license.txt


import frappe
from frappe import _

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)
    
    return columns, data


def get_columns():
    return [
       
        {"label": _("Posting Date/Time"), "fieldname": "posting_datetime", "fieldtype": "Data", "width": 150},

        {"label": _("Tool"), "fieldname": "tool_code", "fieldtype": "Link", "options": "Tool", "width": 150},
        {"label": _("Tool Name"), "fieldname": "tool_name", "fieldtype": "Data", "width": 150},
        {"label": _("Stock UOM"), "fieldname": "stock_uom", "fieldtype": "Link","options": "UOM", "width": 150},
        {"label": _("Current Warehouse"), "fieldname": "current_tool_warehouse", "fieldtype": "Link", "options": "Tool Warehouse", "width": 150},
        {"label": _("Tool Type"), "fieldname": "tool_type", "fieldtype": "Link", "options": "Tool Type", "width": 150},
        {"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 150},
        # {"label": _("Voucher Type"), "fieldname": "voucher_type", "fieldtype": "Data", "width": 150},
        # {"label": _("Voucher #"), "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 150},
        {"label": _("Company"), "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
    ]


def get_conditions(filters):
	conditions = []

	if filters.get("company"):
		conditions.append("tle.company = %(company)s")
	if filters.get("current_tool_warehouse"):
		conditions.append("tle.target_tool_warehouse = %(current_tool_warehouse)s")
	if filters.get("from_date"):
		conditions.append("tle.posting_date >= %(from_date)s")
	if filters.get("to_date"):
		conditions.append("tle.posting_date <= %(to_date)s")
	if filters.get("tool_code"):	
		conditions.append("tle.tool_code = %(tool_code)s")
	if filters.get("voucher_no"):
		conditions.append("tle.voucher_no = %(voucher_no)s")
	if filters.get("tool_type"):
		conditions.append("t.tool_type = %(tool_type)s")

	return " AND ".join(conditions)


def get_data(filters):
    cond = get_conditions(filters)
    if cond:
        cond = " AND " + cond

    query = f"""
        SELECT
            
            CONCAT(
				DATE_FORMAT(tle.posting_date, '%%d-%%m-%%Y'), ' ',
				TIME_FORMAT(tle.posting_time, '%%H:%%i:%%s')
			) AS posting_datetime,
            tle.tool_code AS tool_code,
            COALESCE(t.tool_name, tle.tool_code) AS tool_name,
            COALESCE(t.uom, '') AS stock_uom,
            tle.target_tool_warehouse AS current_tool_warehouse,
            COALESCE(t.tool_type, '') AS tool_type,
            t.description AS description,
             tle.voucher_type AS voucher_type,
             tle.voucher_no AS voucher_no,
            tle.company AS company
        FROM `tabTool Ledger Entry` tle
        LEFT JOIN `tabTool` t ON t.name = tle.tool_code
        
        WHERE tle.docstatus < 2  AND tle.is_cancelled = 0 {cond}
        ORDER BY tle.posting_date ASC, tle.creation ASC
    """

    return frappe.db.sql(query, filters, as_dict=1)
