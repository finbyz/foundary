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
        },
	]
	// ],
	// "treeView": true,
	// "name_field": "task",
	// "parent_field": "parent_task",
	// "initial_depth": 2
};