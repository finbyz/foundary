// frappe.ui.form.on("Sales Order Item", {
//     committed_qty(frm, cdt, cdn) {
//         update_committed_amount(frm, cdt, cdn);
//         calculate_totals(frm);
//     },
//     rate(frm, cdt, cdn) {
//         update_committed_amount(frm, cdt, cdn);
//         calculate_totals(frm);
//     }
// });

// frappe.ui.form.on("Sales Order", {
//     validate(frm) {
//         // Loop through each row in the child table and update
//         frm.doc.items.forEach(row => {
//             update_committed_amount(frm, row.doctype, row.name);
//         });
//         calculate_totals(frm);
//     }
// });

// // Helper function to update committed_amount for a row
// function update_committed_amount(frm, cdt, cdn) {
//     let row = locals[cdt][cdn];

//     let committed_amount = flt(row.committed_qty) * flt(row.rate);
//     let commited_amount_company_currency = 0;

//     if (frm.doc.conversion_rate) {
//         commited_amount_company_currency = committed_amount * flt(frm.doc.conversion_rate);
//     }

//     frappe.model.set_value(cdt, cdn, "committed_amount", committed_amount);
//     frappe.model.set_value(cdt, cdn, "commited_amount_company_currency", commited_amount_company_currency);
// }

// // Helper function to update total committed qty and amount
// function calculate_totals(frm) {
//     let total_qty = 0;
//     let total_amt = 0;
//     let total_committed_amount_inr = 0;

//     frm.doc.items.forEach(row => {
//         total_qty += flt(row.committed_qty);
//         total_amt += flt(row.committed_amount);
//     });

//     if (frm.doc.conversion_rate) {
//         total_committed_amount_inr = flt(total_amt) * flt(frm.doc.conversion_rate);
//     }

//     frm.set_value("total_committed_qty", total_qty);
//     frm.set_value("total_committed_amount", total_amt);
//     frm.set_value("total_commited_amount_inr", total_committed_amount_inr);
// }





frappe.ui.form.on("Sales Order Item", {
    committed_qty(frm, cdt, cdn) {
        update_committed_amount(frm, cdt, cdn);
        calculate_totals(frm);
    },
    rate(frm, cdt, cdn) {
        update_committed_amount(frm, cdt, cdn);
        calculate_totals(frm);
    }
});

frappe.ui.form.on("Sales Order", {
    validate(frm) {
        // Loop through each row in the child table and update
        frm.doc.items.forEach(row => {
            update_committed_amount(frm, row.doctype, row.name);
        });
        calculate_totals(frm);
    }
});

// Helper function to update committed_amount for a row
function update_committed_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    let committed_amount = flt(row.committed_qty) * flt(row.rate);
    let commited_amount_company_currency = 0;

    if (frm.doc.conversion_rate) {
        commited_amount_company_currency = committed_amount * flt(frm.doc.conversion_rate);
    }

    frappe.model.set_value(cdt, cdn, "committed_amount", committed_amount);
    frappe.model.set_value(cdt, cdn, "commited_amount_company_currency", commited_amount_company_currency);
}

// Helper function to update total committed qty and amount
function calculate_totals(frm) {
    let total_qty = 0;
    let total_amt = 0;
    let total_committed_amount_inr = 0;

    frm.doc.items.forEach(row => {
        total_qty += flt(row.committed_qty);
        total_amt += flt(row.committed_amount);
    });

    if (frm.doc.conversion_rate) {
        total_committed_amount_inr = flt(total_amt) * flt(frm.doc.conversion_rate);
    }

    frm.set_value("total_committed_qty", total_qty);
    frm.set_value("total_committed_amount", total_amt);
    frm.set_value("total_commited_amount_inr", total_committed_amount_inr);
}


