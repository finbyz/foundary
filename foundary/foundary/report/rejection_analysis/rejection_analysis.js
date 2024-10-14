// Copyright (c) 2024, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Rejection Analysis"] = {
	"filters": [
		{
			fieldname: 'company',
			label: __('Company'),
			fieldtype: 'Link',
			options: 'Company',
			default: frappe.defaults.get_user_default("Company") 

		},
		{
			fieldname: 'item_group',
			label: __('Item Group'),
			fieldtype: 'Link',
			options: 'Item Group',
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), -7)
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
