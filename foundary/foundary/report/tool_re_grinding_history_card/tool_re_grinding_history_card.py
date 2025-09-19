# Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
# For license information, please see license.txt

# import frappe


import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "History Card No", "fieldname": "card_no", "fieldtype": "Link", "options": "Tool Re-Grinding History Card", "width": 150},
        {"label": "Part No", "fieldname": "part_no", "fieldtype": "Data", "width": 120},
        {"label": "Cutter Specification", "fieldname": "cutter_specification", "fieldtype": "Data", "width": 150},
        {"label": "Tool Type", "fieldname": "types_of_tool", "fieldtype": "Data", "width": 120},
        {"label": "Tool Change Frequency", "fieldname": "tool_change_frequency", "fieldtype": "Data", "width": 120},
        {"label": "Operation", "fieldname": "operation", "fieldtype": "Data", "width": 120},
        {"label": "Tolerance", "fieldname": "tolerance", "fieldtype": "Data", "width": 120},
        {"label": "Tool Life", "fieldname": "tool_life", "fieldtype": "Data", "width": 120},
        {"label": "Run Out", "fieldname": "run_out", "fieldtype": "Data", "width": 120},

        {"label": "Issue Date (MC Shop)", "fieldname": "issue_date_mc_shop", "fieldtype": "Date", "width": 140},
        {"label": "Receive Date (Tooling)", "fieldname": "receive_date_tooling", "fieldtype": "Date", "width": 140},
        {"label": "Re-Grinding Date", "fieldname": "re_grinding_date", "fieldtype": "Date", "width": 140},
        {"label": "Tool Life Qty", "fieldname": "tool_lifeqty", "fieldtype": "Float", "width": 120},
        {"label": "Actual Size", "fieldname": "actual_size", "fieldtype": "Float", "width": 120},
        {"label": "OK / Not OK", "fieldname": "ok__not_ok", "fieldtype": "Data", "width": 100},
        {"label": "Remark", "fieldname": "remark", "fieldtype": "Data", "width": 200},
    ]


def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("card_no"):
        conditions += " AND trghg.name = %(card_no)s"
        values["card_no"] = filters.get("card_no")


    query = f"""
        SELECT
            trghg.name AS card_no,
            trghg.part_no,
            trghg.cutter_specification,
            trghg.types_of_tool,
            trghg.tool_change_frequency,
            trghg.operation,
            trghg.tolerance,
            trghg.tool_life,
            trghg.run_out,

            detail.issue_date_mc_shop,
            detail.receive_date_tooling,
            detail.re_grinding_date,
            detail.tool_lifeqty,
            detail.actual_size,
            detail.ok__not_ok,
            detail.remark

        FROM `tabTool Re-Grinding History Card` trghg
        LEFT JOIN `tabTool Re-grinding History Detail` detail
            ON detail.parent = trghg.name

        WHERE trghg.docstatus < 2 {conditions}
        ORDER BY trghg.creation ASC, detail.idx ASC
    """

    return frappe.db.sql(query, values, as_dict=True)

