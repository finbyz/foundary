# Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
# For license information, please see license.txt



import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data
 

def get_columns():
    return [
        {"label": "Calibration Report No", "fieldname": "report_no", "fieldtype": "Link", "options": "Calibration Report", "width": 150},
        {"label": "Report Date", "fieldname": "report_date", "fieldtype": "Date", "width": 120},
        {"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date", "width": 120},
        {"label": "Tool Code", "fieldname": "tool_code", "fieldtype": "Data", "width": 150},
        {"label": "Tool Name", "fieldname": "tool_name", "fieldtype": "Data", "width": 150},
        {"label": "Company", "fieldname": "company", "fieldtype": "Data", "width": 180},
        {"label": "Calibration Type", "fieldname": "calibration_type", "fieldtype": "Data", "width": 120},
        {"label": "Calibration Template", "fieldname": "calibration_template", "fieldtype": "Data", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
       

        # Child Table fields
        {"label": "Parameter", "fieldname": "parameter", "fieldtype": "Data", "width": 180},
        {"label": "Minimum Value", "fieldname": "minimum_value", "fieldtype": "Float", "width": 120},
        {"label": "Maximum Value", "fieldname": "maximum_value", "fieldtype": "Float", "width": 120},
        {"label": "Reading", "fieldname": "reading_1", "fieldtype": "Float", "width": 120},
        {"label": "Remarks", "fieldname": "remarks", "fieldtype": "Data", "width": 150},
    ]


def get_data(filters):
	conditions = ""
	values = {}

	if filters.get("report_no"):
		conditions += " AND cr.name = %(report_no)s"
		values["report_no"] = filters.get("report_no")

	if filters.get("company"):
		conditions += " AND cr.company = %(company)s"
		values["company"] = filters.get("company")
	if filters.get("from_date"):
		conditions += " AND cr.report_date >= %(from_date)s"
		values["from_date"] = filters.get("from_date")

	if filters.get("to_date"):
		conditions += " AND cr.report_date <= %(to_date)s"
		values["to_date"] = filters.get("to_date")

	query = f"""
		SELECT
			cr.name AS report_no,
			cr.report_date,
			cr.due_date,
			cr.tool_code,
			cr.tool_name,
			cr.company,
			cr.calibration_type,
			cr.calibration_template,
			cr.status,
			crr.parameter,
			crr.minimum_value,
			crr.maximum_value,
			crr.reading_1,
			crr.remarks

		FROM `tabCalibration Report` cr
		LEFT JOIN `tabCalibration Report Reading` crr
			ON crr.parent = cr.name

		WHERE cr.docstatus = 1 {conditions}
		ORDER BY cr.creation ASC, crr.idx ASC
	"""

	return frappe.db.sql(query, values, as_dict=True)

