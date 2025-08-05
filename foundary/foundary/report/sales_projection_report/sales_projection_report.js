// Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Projection Report"] = {

	onload: function(report) {
        frappe.call({
            method: "foundary.foundary.report.sales_projection_report.sales_projection_report.get_current_fiscal_year",
            callback: function(r) {
                if (r.message) {
                    report.set_filter_value("financial_year", r.message);
                }
            }
        });
		const currentMonth = frappe.datetime.str_to_obj(frappe.datetime.get_today()).toLocaleString('default', { month: 'long' });
        report.page.fields_dict.month.set_value(currentMonth);
    },

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
		},
		{
			"fieldname": "month",
			"label": "Month",
			"fieldtype": "Select",
			"options": "\nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember",
		},
		{
			"fieldname": "financial_year",
			"label": "Financial Year",
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": frappe.defaults.get_default("fiscal_year")
		}
	]
};
