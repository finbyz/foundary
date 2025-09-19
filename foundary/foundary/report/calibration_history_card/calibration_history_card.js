// Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt

frappe.query_reports["Calibration History Card"] = {
	  "filters": [
        {
            "fieldname": "report_no",
            "label": __("Calibration Report No"),
            "fieldtype": "Link",
            "options": "Calibration Report",
            "reqd": 0,
            "width": "150px"
        },
       
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 0
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 0
        },
		 {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 0,
            "width": "150px"
        }
    ],
	 formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (column.fieldname == "reading_1" && data) {
            let readingVal = parseFloat(data.reading_1) || 0;
            let maxVal = parseFloat(data.maximum_value) || 0;
            let minVal = parseFloat(data.minimum_value) || 0;

            if (readingVal > maxVal || readingVal < minVal) {
                value = `<span style="color:red;">${readingVal}</span>`;
            }
			else if(readingVal == 0){
				value = `<span >${readingVal}</span>`;
			}
			else {
                value = `<span style="color:green;">${readingVal}</span>`;
            }
        }

        return value;
    }
};




