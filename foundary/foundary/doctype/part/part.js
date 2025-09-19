// Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on("Part", {
	 onload: function(frm) {
        frm.fields_dict["required_tools"].grid.get_field("tool_code").get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                    disable: 0  
                }
            };
        };
    },
     part_no: function(frm) {
        if (!frm.doc.part_name) {
            frm.set_value("part_name", frm.doc.part_no);
        }
    }
});
