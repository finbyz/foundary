// Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Projection Report"] = {
	"filters": [
		{
		"fieldname": "company",
		"label": "Company",
		"fieldtype": "Link",
		"options": "Company",
		"default": "RBD Engineers Pvt Ltd",
		"reqd": 0
		},
		{
		"fieldname": "from_date",
		"label": "From Date",
		"fieldtype": "Date",
		"reqd": 0
		},
		{
		"fieldname": "to_date",
		"label": "To Date",
		"fieldtype": "Date",
		"reqd": 0
		}
	]
};
