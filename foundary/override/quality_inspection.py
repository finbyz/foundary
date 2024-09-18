import frappe
from frappe import _
from erpnext.stock.doctype.quality_inspection.quality_inspection import QualityInspection as _quality_inspection
from foundary.foundary.doc_events.quality_inspection import get_template_details


class QualityInspection(_quality_inspection):
    def validate(self):
        if not self.readings and self.item_code:
            self.get_item_specification_details()

        if self.inspection_type == "In Process" and self.reference_type == "Job Card":
            item_qi_template = frappe.db.get_value("Item", self.item_code, "quality_inspection_template")
            parameters = get_template_details(item_qi_template)
            for reading in self.readings:
                for d in parameters:
                    if reading.specification == d.specification:
                        reading.update(d)
                        reading.status = "Accepted"

        if self.readings:
            self.inspect_and_set_status()

    def before_submit(self):
        self.validate_readings_status_mandatory()

    @frappe.whitelist()
    def get_item_specification_details(self):
        if not self.quality_inspection_template:
            self.quality_inspection_template = frappe.db.get_value(
                "Item", self.item_code, "quality_inspection_template"
            )

        if not self.quality_inspection_template:
            return

        self.set("readings", [])
        parameters = get_template_details(self.quality_inspection_template)
        for d in parameters:
            child = self.append("readings", {})
            child.update(d)
            child.status = "Accepted"

    @frappe.whitelist()
    def get_quality_inspection_template(self):
        template = ""
        if self.bom_no:
            template = frappe.db.get_value("BOM", self.bom_no, "quality_inspection_template")

        if not template:
            template = frappe.db.get_value("BOM", self.item_code, "quality_inspection_template")

        self.quality_inspection_template = template
        self.get_item_specification_details()

    def on_submit(self):
        self.update_qc_reference()

    def on_cancel(self):
        self.update_qc_reference()