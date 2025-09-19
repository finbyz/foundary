// Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on("Tool Request", {
   
   refresh: function(frm) {
        if (!frm.is_new() && (frm.doc.docstatus === 0 || frm.doc.docstatus === 1)) {
           
            frm.add_custom_button(
                __("Tool Movement"),
                function() {
                    frappe.model.open_mapped_doc({
                        method: "foundary.foundary.doctype.tool_request.tool_request.make_tool_movement",
                        frm: frm
                    });
                },
                __("Create")
            );
        }
    },
    onload: function(frm) {
        frm.fields_dict["tool_request_details"].grid.get_field("tool_name").get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                    disable: 0  
                }
            };
        };
    },
    source_tool_warehouse: function (frm) {
    frm.set_query("target_tool_warehouse", function () {
      return {
        filters: [
          ["Tool Warehouse", "name", "!=", frm.doc.source_tool_warehouse]
        ]
      };
    });
  },

  target_tool_warehouse: function (frm) {
    frm.set_query("source_tool_warehouse", function () {
      return {
        filters: [
          ["Tool Warehouse", "name", "!=", frm.doc.target_tool_warehouse]
        ]
      };
    });
  }
,
   part_no: function (frm) {
        if (!frm.doc.part_no) {
            // If part is removed, clear child table
            frm.clear_table("tool_request_details");
            frm.refresh_field("tool_request_details");
            return;
        }

        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Part",   
                name: frm.doc.part_no   
            },
            callback: function (r) {
                if (r.message) {
                    const part = r.message;

                    // Clear existing child table
                    frm.clear_table("tool_request_details");

                    // Loop through required tools in Part Master
                    (part.required_tools || []).forEach((tool) => {
                        let row = frm.add_child("tool_request_details");
                        row.tool_name = tool.tool_code;  
                        row.source_tool_warehouse = tool.warehouse;
                        row.required_by = frm.doc.required_by;
                    });

                    frm.refresh_field("tool_request_details");
                }
            }
        });
    }
});


frappe.ui.form.on("Tool Request Details", {
    
    tool_request_details_add(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);

        
        row.required_by = frm.doc.required_by;
        row.source_tool_warehouse = frm.doc.source_tool_warehouse;
        row.target_tool_warehouse = frm.doc.target_tool_warehouse;

        frm.refresh_field("tool_request_details");
    }
});




