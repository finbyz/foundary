frappe.ui.form.on('Payment Entry',  {
    party: function(frm) {
        
        if (frm.doc.party) {
            frappe.call({
                method: "foundary.foundary.doc_events.payment_entry.get_party_details",
                args: {
                    party: frm.doc.party
                },
                callback: function(r) {
                    if (r.message.len==1) {
                        frm.set_value('party_bank_account', r.message.data[0].name);
                        frm.set_value('ifs_code', r.message.data[0].ifs_code);
                        frm.set_value('bank_acc_no', r.message.data[0].bank_account_no);
                        frm.refresh_field(["party_bank_account", "ifs_code", "bank_acc_no"]);
                    }
                    
                }
            });
        }
                
    },
    before_save: function(frm) {
        
        if (frm.doc.party) {
            frappe.call({
                method: "foundary.foundary.doc_events.payment_entry.get_party_details",
                args: {
                    party: frm.doc.party
                },
                callback: function(r) {
                    console.log(r.message.len)
                    if (r.message.len==1) {
                            frm.set_value('party_bank_account', r.message.data[0].name);
                            frm.set_value('ifs_code', r.message.data[0].ifs_code);
                            frm.set_value('party_bank_account_no', r.message.data[0].bank_account_no);
                            frm.refresh_field(["party_bank_account", "ifs_code", "party_bank_account_no"]);
                    }
                    
                }
            });
        }
                
    }

});