// Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt


frappe.ui.form.on("Tool Movement", {
   refresh: function(frm) {
        if (!frm.is_new() &&  frm.doc.docstatus === 1) {

            // View Tool Ledger
            frm.add_custom_button(__('Tool Ledger'), function() {
                frappe.set_route('query-report', 'Tool Ledger', {
                    company: frm.doc.company,
                    from_date: frappe.datetime.add_months(frm.doc.date, -1),
                    to_date: frm.doc.date,
                    voucher_no: frm.doc.name,
                 
                });
            }, __('View'));

            // View Tool Balance
            frm.add_custom_button(__('Tool Balance'), function() {
                frappe.set_route('query-report', 'Tool Balance', {
                    company: frm.doc.company,
                    from_date: frappe.datetime.add_months(frm.doc.date, -1),
                    to_date: frm.doc.date,
                    voucher_no: frm.doc.name,
                    
                });
            }, __('View'));
        }
    },
   
  onload: function (frm) {

    // Set dynamic filters for source_warehouse and target_warehouse in child table
    frm.fields_dict["tool_movement_details"].grid.get_field("source_warehouse").get_query = function (doc, cdt, cdn) {
      const row = locals[cdt][cdn];
      return {
        filters: [
          ["Tool Warehouse", "name", "!=", row.target_warehouse]
        ]
      };
    };

    frm.fields_dict["tool_movement_details"].grid.get_field("target_warehouse").get_query = function (doc, cdt, cdn) {
      const row = locals[cdt][cdn];
      return {
        filters: [
          ["Tool Warehouse", "name", "!=", row.source_warehouse]
        ]
      };
    };


    // Set dynamic filters for Tool Name in child table
      frm.fields_dict["tool_movement_details"].grid.get_field("tool_code").get_query = function(doc, cdt, cdn) {
          return {
              filters: {
                  disable: 0  
              }
          };
      };
    
    // Add filter for Target Tool Warehouse
    frm.set_query("target_tool_warehouse", function () {
      return {
        filters: [
          ["Tool Warehouse", "name", "!=", frm.doc.source_tool_warehouse]
        ]
      };
    });

    // Optional: Filter for Source Tool Warehouse as well (to avoid selecting same if target is already set)
    frm.set_query("source_tool_warehouse", function () {
      return {
        filters: [
          ["Tool Warehouse", "name", "!=", frm.doc.target_tool_warehouse]
        ]
      };
    });
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
});



frappe.ui.form.on("Tool Movement Details", {
    tool_movement_details_add(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        row.source_warehouse = frm.doc.source_tool_warehouse;
        row.target_warehouse = frm.doc.target_tool_warehouse;
        frm.refresh_field("tool_movement_details");
    }
});


