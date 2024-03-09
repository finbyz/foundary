frappe.ui.form.on('Job Card',  {
    before_save: function(frm) {
        frm.clear_table('scrap_items');
        var child = frm.add_child("scrap_items");
        child.item_code = frm.doc.production_item;
        child.item_name = frm.doc.item_name;
        child.stock_qty = frm.doc.process_loss_qty; 
    },
    rejections_add: function(frm) {
    }
});
// frappe.ui.form.on('Job Card Rejections',  {
//     rejections_add: function(frm,cdt,cdn) {
//         frappe.model.set_value(cdt, cdn, 'rejection_percentage', qty/frm.doc.total_completed_qty);
//         frm.refresh_field('rejections');
//     }
// });