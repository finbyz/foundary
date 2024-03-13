import frappe
from frappe.model.document import Document

def get_template_details(template):
	if not template:
		return []

	return frappe.get_all(
		"Item Quality Inspection Parameter",
		fields=[
			"specification",
			"value",
			"acceptance_formula",
			"numeric",
			"remarks",
			"test_method",
			"formula_based_criteria",
			"special_characteristics",
			"min_value",
			"max_value",
		],
		filters={"parenttype": "Quality Inspection Template", "parent": template},
		order_by="idx",
	)
