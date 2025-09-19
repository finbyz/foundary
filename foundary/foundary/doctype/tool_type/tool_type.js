// Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt
frappe.ui.form.on("Tool Type", {
	onload(frm) {
		frm.fields_dict["parent_tool_type"].get_query = function (doc) {
			return {
				filters: [
					["Tool Type", "is_group", "=", 1],
					["Tool Type", "name", "!=", doc.tool_type_name]
				]
			};
		};
	}
});

