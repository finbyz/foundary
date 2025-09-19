// Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt


frappe.query_reports["Tool Ledger"] = {
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
            "fieldname": "default_tool_warehouse",
            "label": __("Warehouse"),
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
,


	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		console.log("data", data);
		
		if (column.fieldname == "source_tool_warehouse" && data && data.source_tool_warehouse) {
			value = "<span style='color:red'>" + value + "</span>";
		} else if (column.fieldname == "target_tool_warehouse" && data && data.target_tool_warehouse) {
			value = "<span style='color:green'>" + value + "</span>";
		}
		

		return value;
	},


};
