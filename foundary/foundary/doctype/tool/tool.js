// Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on("Tool", {

    refresh: function(frm) {
        // clear previous custom buttons (to avoid duplicates)
         frm.page.$title_area.find(".calibration-btn").remove();
         frm.page.$title_area.find(".custom-warehouse-btn").remove();
         
        if (frm.doc.tool_code) {
            
    frappe.call({
        method: "foundary.foundary.doctype.tool.tool.get_latest_tool_movement",
        args: {
            tool_code: frm.doc.tool_code
        },
        callback: function(r) {
            if (r.message && r.message.name) {
                let latest = r.message;
                let tool_movement_details = latest.doc.tool_movement_details || [];

                //  Keep track of unique warehouses
                let warehouses = new Set();

                for (let tool_data of tool_movement_details) {
                    if (frm.doc.tool_code == tool_data.tool_code && tool_data.target_warehouse) {
                        warehouses.add(tool_data.target_warehouse);
                      
                    }
                }

                // Add only unique buttons
                warehouses.forEach(wh => {
                    let btn = frm.add_custom_button(wh, function() {
                        // your logic
                    });

                    $(btn)
                        .removeClass("btn-default")
                        .addClass("btn-success custom-warehouse-btn")
                        .appendTo(frm.page.$title_area);
                });
            }
            else if (frm.doc.default_tool_warehouse) {
                let btn = frm.add_custom_button(frm.doc.default_tool_warehouse, function() {
                    // your logic
                });

                $(btn)
                    .removeClass("btn-default")
                    .addClass("btn-success custom-warehouse-btn")
                    .appendTo(frm.page.$title_area);
            }
        }
    });
}
        
        // --- Calibration logic ---
        
        if (frm.doc.calibration_details && frm.doc.calibration_details.length > 0) {
            console.log("Calibration Details:", frm.doc.calibration_details);
            // Find latest calibration entry by report_date
            frm.page.$title_area.find(".calibration-btn").remove();
            
            let latest = frm.doc.calibration_details
                .filter(row => row.due_date)  // keep only records having due_date
                .sort((a, b) => new Date(b.due_date) - new Date(a.due_date))[0];
            

            if (latest && latest.due_date) {
                let today = frappe.datetime.get_today();

                // Clear previous custom buttons (to avoid duplicates)
                frm.clear_custom_buttons();
               
             
                
                if (latest.due_date < today) {
                    // Calibration valid → show Disable button
                    let btn = frm.add_custom_button("Disable Tool", function() {
                        
                    });
                     
                let label = $(`
                    <span class="calibration-btn ml-2 px-2 py-1 text-white bg-danger"
                        style="
                            border-radius: 8px;
                            display: inline-flex;
                            align-items: center;
                            white-space: nowrap;
                            max-width: 150px;
                            overflow: hidden;
                            text-overflow: ellipsis;
                        ">
                        Calibration Due
                    </span>
                `);

                

                // Append it right after warehouse buttons in title area
                frm.page.$title_area.append(label);

                       if (frm.doc.disable !== 1) {   
                        frm.set_value("disable", 1);
                        frm.save();
                    }
                 

                   
                } else {
                    // Calibration expired → show Enable button
                   let btn = frm.add_custom_button("Enable Tool", function() {
                        
                    });
                     if (frm.doc.disable !== 0) {   
                        frm.set_value("disable", 0);
                        frm.save();
                    }
                    
                }
            }
        }


        // --- End Calibration logic ---

    },

    tool_code: function(frm) {
        if (!frm.doc.tool_name) {
            frm.set_value("tool_name", frm.doc.tool_code);
        }
    }
});
