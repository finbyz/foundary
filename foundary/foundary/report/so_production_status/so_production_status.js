// Copyright (c) 2023, FinByz Tech Pvt Ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["SO Production Status"] = {
	"filters": [
        {
            fieldname: 'company',
            label: __('Company'),
            fieldtype: 'Link',
            options: 'Company',
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1
        },
		{
			fieldname: "item_code",
			label: __("Item Code"),
			fieldtype: "Link",
			options:"Item"
		},
		{
			fieldname: "delivery_upto",
			label: __("Delivery Upto"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
	]
	// ],
	// "treeView": true,
	// "name_field": "task",
	// "parent_field": "parent_task",
	// "initial_depth": 2
};