frappe.ui.form.on('BOM',  {
    
});

frappe.ui.form.on("BOM Additional Cost", {
	qty: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
	},
    rate: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    }
    
});

var calculate_amount = function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];

    if(d.qty && d.rate){
        d.amount = d.qty * d.rate
    }

    refresh_field("amount", d.name, d.parentfield)
}
