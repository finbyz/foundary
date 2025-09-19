// Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt


frappe.ui.form.on("Tool Warehouse", {
  onload: function (frm) {
    frm.list_route = "Tree/Tool Warehouse";

    frm.fields_dict["parent_tool_warehouse"].get_query = function (doc) {
      return {
        filters: [
          ["Tool Warehouse", "is_group_tool_warehouse", "=", 1],
          ["Tool Warehouse", "name", "!=", doc.tool_warehouse_name]
        ]
      };
    };
  }
});