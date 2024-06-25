# Copyright (c) 2024, Finbyz Tech PVT LTD and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
import re
from frappe import _

def execute(filters=None):
	if filters.get("from_date") and filters.get("to_date"):
		if filters.get("from_date") > filters.get("to_date"):
			frappe.throw(_("From Date cannot be less than To Date"))

	columns, data = get_data(filters)
	chart = get_chart_data(filters)
	return columns, data, None, chart

def get_data(filters):
	conditions = ""
	if filters.get("from_date") and filters.get("to_date"):
		conditions = " and Date(jc.creation) between '{0}' and '{1}'".format(filters.get("from_date"), filters.get("to_date"))
	if filters.get("item_group"):
		conditions += " and i.item_group = '{0}'".format(filters.get("item_group"))
	if filters.get("company"):
		conditions += " and jc.company = '{0}'".format(filters.get("company"))
	job_card_data = frappe.db.sql(f""" 
	SELECT
		jc.production_item AS item,
		SUM(jc.for_quantity) AS qty_to_manufacture,
		SUM(jc.total_completed_qty) AS manufactured_qty,
		SUM(jc.process_loss_qty) AS total_rejected,
		SUM(jc.process_loss_qty * i.weight_per_unit) AS rejected_qty_weight,
		SUM(jc.total_completed_qty * i.weight_per_unit) AS production_weight,
		Sum(jc.process_loss_qty * i.weight_per_unit) / Sum(jc.total_completed_qty * i.weight_per_unit) * 100 AS weight_rejected_percentage
	FROM 
		`tabJob Card` jc
	JOIN 
		`tabItem` i ON jc.production_item = i.item_code
	WHERE
		jc.status = 'Completed'{conditions} and jc.docstatus = 1
	GROUP BY 
		jc.production_item
	ORDER BY
		jc.creation DESC
	""",as_dict=True)

	job_card_rejection_data = frappe.db.sql(f""" 
	SELECT
		jc.production_item AS item,
		jcr.reason_id,
		Sum(jcr.qty) as rejected_qty
	FROM 
		`tabJob Card Rejections` jcr
	Left JOIN 
		`tabJob Card` jc ON jcr.parent = jc.name	
	JOIN `tabItem` i ON jc.production_item = i.item_code					  
	WHERE
		jc.status = 'Completed'{conditions} and jc.docstatus = 1
	GROUP BY 
		jc.production_item,jcr.reason_id
	ORDER BY
		jc.creation DESC
	""",as_dict=True)
	reasons = []
	for i in job_card_rejection_data:
		reasons.append(i.reason_id)
	data = []
	unique_data = {}

	columns = [
		{"label": _("Item"), "fieldname": "item", "fieldtype": "Link", "options": "Item", "width": 150},
		{"label": _("QTY To Manufacture"), "fieldname": "qty_to_manufacture", "fieldtype": "Float", "width": 200},
		{"label": _("Manufactured Qty"), "fieldname": "manufactured_qty", "fieldtype": "Float", "width": 200},
		{"label": _("Total Rejected"), "fieldname": "total_rejected", "fieldtype": "Float", "width": 100},
		{"label": _("Rejected Percentage"), "fieldname": "rejected_percentage", "fieldtype": "Percent", "width": 100},
		{"label": _("Rejected Qty Weight"), "fieldname": "rejected_qty_weight", "fieldtype": "Float", "width": 150},
		{"label": _("Production Weight"), "fieldname": "production_weight", "fieldtype": "Float", "width": 150},
		{"label": _("Weight Rejected Percentage"), "fieldname": "weight_rejected_percentage", "fieldtype": "Percent", "width": 150}
	]

	unique_reason = []
	for reason in reasons:
		if reason not in unique_reason:
			columns.append({"label": _(f"{reason}"), "fieldname": f"{reason}", "fieldtype": "Data", "width": 80,"align":"right"})
			unique_reason.append(reason)
	iwb_map = {}
	for d in job_card_rejection_data:
		if d.item not in iwb_map:
			iwb_map[d.item] = {}
		iwb_map[d.item][d.reason_id] = d.rejected_qty
	for row in job_card_data:
		unique_data.update({row.item : {}})
		unique_data[row.item].update({
			"item": row.item,"qty_to_manufacture":row.qty_to_manufacture,"manufactured_qty":row.manufactured_qty,
			"total_rejected":row.total_rejected,"rejected_percentage":str(row.total_rejected/row.qty_to_manufacture*100) + "%",
			"rejected_qty_weight":row.rejected_qty_weight,"production_weight":row.production_weight,
			"weight_rejected_percentage":row.weight_rejected_percentage
		})

		unique_data[row.item].update(iwb_map.get(row.item,{}))


	data = []
	for row in unique_data:
		data.append(unique_data[row])


	return columns, data

def get_chart_data(filters):
	conditions = ""
	if filters.get("from_date") and filters.get("to_date"):
		conditions = " and Date(jc.creation) between '{0}' and '{1}'".format(filters.get("from_date"), filters.get("to_date"))
	if filters.get("item_group"):
		conditions += " and i.item_group = '{0}'".format(filters.get("item_group"))
	if filters.get("company"):
		conditions += " and jc.company = '{0}'".format(filters.get("company"))
		
	job_card_data = frappe.db.sql(f""" 
	SELECT
		jc.production_item AS item,
		SUM(jc.process_loss_qty) AS total_rejected
	FROM 
		`tabJob Card` jc
	WHERE
		jc.status = 'Completed'{conditions} and jc.docstatus = 1
	GROUP BY 
		jc.production_item
	ORDER BY
		total_rejected DESC
	LIMIT 10
	""",as_dict=True)

	custom_labels = []
	custom_values = []

	for i in job_card_data:
		custom_labels.append(i.item)
		custom_values.append(i.total_rejected)

	chart = {
		"data": {
			"labels": custom_labels,
			"datasets": [{"name": _("Total Rejected"), "values": custom_values}],
		},
		"type": "bar",
		"fieldtype": "data",
	}

	return chart
