frappe.ui.form.on('Job Card',  {
    before_save: function(frm) {
        frm.clear_table('scrap_items');
        var child = frm.add_child("scrap_items");
        child.item_code = frm.doc.production_item;
        child.item_name = frm.doc.item_name;
        child.stock_qty = frm.doc.process_loss_qty;
    }
});