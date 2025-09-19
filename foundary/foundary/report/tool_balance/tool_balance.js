// Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt


frappe.query_reports["Tool Balance"] = {
    "filters": [

		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			
		},
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            
        },
       
        {
            "fieldname": "current_tool_warehouse",
            "label": __("Current Warehouse"),
            "fieldtype": "Link",
            "options": "Tool Warehouse"
        },
		 {
            "fieldname": "tool_code",
            "label": __("Tool"),
            "fieldtype": "Link",
            "options": "Tool"
        },
		{
			fieldname: "tool_type",
			label: __("Tool Type"),
			fieldtype: "Link",
			options: "Tool Type",
		},
		{
			fieldname: "voucher_no",
			label: __("Voucher #"),
			fieldtype: "Data",
		},
    ]
};
