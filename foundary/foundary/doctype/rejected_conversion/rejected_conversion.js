// Copyright (c) 2024, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rejected Conversion', {
	// refresh: function(frm) {
	company:function(frm){
		frappe.db.get_value('Company', frm.doc.company, 'scrap_rejected_warehouse', (r) => {
			if (r && r.scrap_rejected_warehouse) {
				frm.set_value('scrap_rejected_warehouse', r.scrap_rejected_warehouse);
			}
		});
		frappe.db.get_value('Company', frm.doc.company, 'scrap_item', (r) => {
			if (r && r.scrap_item) {
				frm.set_value('scrap_item', r.scrap_item);
			}
		});
		frappe.db.get_value('Company', frm.doc.company, 'scrap_target_warehouse', (r) => {
			if (r && r.scrap_target_warehouse) {
				frm.set_value('scrap_target_warehouse', r.scrap_target_warehouse);
			}
		});
	},
	onload: function(frm) {
		frm.set_query("scrap_rejected_warehouse",function(){
			return {
				filters:{
					"company" : frm.doc.company,
					"is_group": 0
				}
			}
		});
		frm.set_value("scrap_rejected_warehouse","")
		frm.set_value("scrap_target_warehouse","")
		frm.set_value("scrap_item","")
		frm.set_query("scrap_target_warehouse",function(){
			return {
				filters:{
					"company" : frm.doc.company,
					"is_group": 0
				}
			}
		});
	},
	get_items:function(frm){
		console.log("function called");

		if (frm.doc.company){
			frm.doc.item = [];

			frm.call({
				doc: frm.doc,
				method: "get_rejected_items",				
			}).then((r) => {
				r.message.forEach(element => {
					var item = frm.add_child("item");

					item.item_code = element['item_code'];
					item.item_name = element['item_name'];
					item.qty = element['qty'];

					frm.refresh_field("item");
				});
			});

			frm.refresh_field("item");
		}


	}
	// }
});
