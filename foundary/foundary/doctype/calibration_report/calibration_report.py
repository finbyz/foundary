# Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document


class CalibrationReport(Document):
   
    def on_cancel(self):
        if hasattr(self, "status"):
            self.db_set("status", "Cancelled")

        # Remove this report from the tool's calibration details
        if self.tool_code:
            tool = frappe.get_doc("Tool", self.tool_code)

            rows_to_remove = [d for d in tool.calibration_details if d.reference_id == self.name]
           
            for d in rows_to_remove:
                tool.remove(d)

            tool.save(ignore_permissions=True)
        

    def on_submit(self):
        if not self.tool_code:
            return

        try:
            tool = frappe.get_doc("Tool", self.tool_code)

            
            tool.append("calibration_details", {
                "reference_id": self.name,
                
                "report_date": self.report_date,
                "due_date": self.due_date,
                "status": self.status,
                "calibration_type": self.calibration_type
            })

            
            tool.save(ignore_permissions=True)
            

        except Exception as e:
            frappe.log_error(title="Calibration Report - Tool update failed",message=frappe.get_traceback())
            
            
        