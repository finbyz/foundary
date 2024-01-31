import frappe
from frappe.utils import flt

def before_validate(self, method):
		validate_update_amount(self)
		
def validate_update_amount(self):
	for row in self.additional_cost:
		row.qty = self.quantity
		row.amount = flt(flt(row.qty) * flt(row.rate))