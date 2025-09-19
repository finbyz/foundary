// Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on("Calibration Report", {

  refresh:function(frm) {
        console.log("Form refreshed",frm);
        
        frm.fields_dict["calibration_report_reading"].grid.grid_rows.forEach(row => {
            highlight_calibration_cell(frm, row.doc.doctype, row.doc.name);
        });
    },

  onload: function(frm) {
       frm.set_query("tool_code", function() {
            return {
                filters: {
                    disable: 0
                }
            };
        });
    },

   report_date: function(frm) {
        if (frm.doc.report_date) {
            console.log("report_date changed", frm.doc.report_date);

            // Convert report_date (string) → Date object
            let report_date = frappe.datetime.str_to_obj(frm.doc.report_date);

            // Add 12 months (equivalent to 1 year)
            let due_date = frappe.datetime.add_months(report_date, 12);
            due_date = frappe.datetime.add_days(due_date, -1);

            // Set due_date back to form
            frm.set_value("due_date", frappe.datetime.obj_to_str(due_date));
        }
    },
  calibration_template: function (frm) {
    if (!frm.doc.calibration_template) {
      // If template is removed, clear the child table
      frm.clear_table("calibration_report_reading");
      frm.refresh_field("calibration_report_reading");
      return;
    }

    frappe.call({
      method: "frappe.client.get",
      args: {
        doctype: "Calibration Template",
        name: frm.doc.calibration_template,
      },
      callback: function (r) {
        if (r.message) {
          const template = r.message;

          // Clear existing rows first
          frm.clear_table("calibration_report_reading");

          // Loop through each item_calibration_parameter and add to child table
          (template.item_calibration_parameter || []).forEach((param) => {
            const row = frm.add_child("calibration_report_reading");
            row.parameter = param.parameter;
            row.minimum_value = param.minimum_value;
            row.maximum_value = param.maximum_value;
            row.reading_1 = param.reading_1;
          });

          frm.refresh_field("calibration_report_reading");
        }
      },
    });
  },
});



frappe.ui.form.on("Calibration Report Reading", {
    reading_1: function(frm, cdt, cdn) {
        highlight_calibration_cell(frm, cdt, cdn);
    },
    calibration_report_reading_add: function(frm, cdt, cdn) {
       highlight_calibration_cell(frm, cdt, cdn);

    }
   
    
});

function highlight_calibration_cell(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let readingVal = parseFloat(row.reading_1) || 0;
    let maxVal = parseFloat(row.maximum_value) || 0;
    let minVal = parseFloat(row.minimum_value) || 0;

    let grid_row = frm.fields_dict["calibration_report_reading"].grid.grid_rows_by_docname[cdn];
    if (grid_row) {
        // target both input and static area (when not focused)
        let $cell = $(grid_row.row).find('[data-fieldname="reading_1"]');
      
       let color = ""
       if (readingVal > maxVal || readingVal < minVal) {
           color = "red";
          }
          else{
            color = "green";
          }
        $cell.css("color", color);
    }
}
