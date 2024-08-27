import frappe

def before_validate(self,method):
	update_manual_inspection(self)
	
def update_manual_inspection(self):
	for i in self.readings:
		if i.numeric == 0:
			i.manual_inspection = 1

	# if not self.quality_inspection_template:
	# 	self.quality_inspection_template = frappe.db.get_value(
	# 		"Item", self.item_code, "quality_inspection_template"
	# 	)

	# if not self.quality_inspection_template:
	# 	return

	# self.set("readings", [])
	# parameters = get_template_details(self.quality_inspection_template)
	# for d in parameters:
	# 	child = self.append("readings", {})
	# 	child.update(d)
	# 	child.status = "Accepted"

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