import frappe
from frappe import _
import erpnext
from erpnext.manufacturing.doctype.bom.bom import BOM
from frappe.utils import cint, cstr, flt, today

class CustomBOM(BOM):
    def calculate_op_cost(self, update_hour_rate=False):
            """Update workstation rate and calculates totals"""
            self.operating_cost = 0
            self.base_operating_cost = 0
            if self.get("with_operations"):
                for d in self.get("operations"):
                    if d.workstation_type:
                        self.update_rate_and_time(d, update_hour_rate)

                    operating_cost = d.operating_cost
                    base_operating_cost = d.base_operating_cost
                    if d.set_cost_based_on_bom_qty:
                        operating_cost = flt(d.cost_per_unit) * flt(self.quantity)
                        base_operating_cost = flt(d.base_cost_per_unit) * flt(self.quantity)

                    self.operating_cost += flt(operating_cost)
                    self.base_operating_cost += flt(base_operating_cost)

            elif self.get("fg_based_operating_cost"):
                total_operating_cost = flt(self.get("quantity")) * flt(
                    self.get("operating_cost_per_bom_quantity")
                )
                self.operating_cost = total_operating_cost
                self.base_operating_cost = flt(total_operating_cost * self.conversion_rate, 2)
    def update_rate_and_time(self, row, update_hour_rate=False):
	    if not row.hour_rate or update_hour_rate:
                hour_rate = flt(frappe.get_cached_value("Workstation Type", row.workstation_type, "hour_rate"))
                if hour_rate:
                    row.hour_rate = (
                            hour_rate / flt(self.conversion_rate) if self.conversion_rate and hour_rate else hour_rate
                        )