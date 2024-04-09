// Copyright (c) 2024, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Rejection Analysis"] = {
	"filters": [
		{
			fieldname: 'item_group',
			label: __('Item Group'),
			fieldtype: 'Link',
			options: 'Item Group',
		},
		{
			fieldname: 'company',
			label: __('Company'),
			fieldtype: 'Link',
			options: 'Company',
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today()
		},
	]
};
