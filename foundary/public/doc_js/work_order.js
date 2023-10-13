frappe.ui.form.on('Work Order', {
	refresh: function(frm) {
		if (frm.doc.__islocal) {
			if (frm.doc.bom_no) {
				return frm.call({
					doc: frm.doc,
					method: "get_items_and_operations_from_bom",
					freeze: true,
					callback: function(r) {
						if(r.message["set_scrap_wh_mandatory"]) {
							frm.toggle_reqd("scrap_warehouse", true);
						}
					}
				});
			}
		}
	},
	validate: function(frm) {
		if (frm.doc.__islocal) {
			if (frm.doc.source_warehouse) {
				$.each(frm.doc.required_items, function(i, d) {
					if (!d.source_warehouse) {
						frappe.model.set_value(d.doctype, d.name, 'source_warehouse', frm.doc.source_warehouse);
					}
				});
			}
		}
	}
});