import frappe

def on_update(self, method):
	if method == "submit":
		validate_update_qty(self)


def validate_update_qty(self):
	self.last_qty = 0
	total_idx = [
		item[0]
		for item in frappe.db.get_list(
			"Work Order Operation",
			{"parent": self.work_order},
			"sequence_id",
			order_by="sequence_id asc",
			as_list=True,
		)
	]
	completed_qty, process_loss_qty = frappe.db.get_value(
		"Work Order Operation",
		{"parent": self.work_order, "sequence_id": self.sequence_id},
		["completed_qty", "process_loss_qty"],
	)
	first_idx = total_idx[0] if total_idx else 1

	if self.sequence_id == first_idx:
		qty_to_manufacture = frappe.db.get_value("Work Order", self.work_order, "qty")
	else:
		qty_to_manufacture = frappe.db.get_value(
			"Work Order Operation",
			{
				"parent": self.work_order,
				"sequence_id": total_idx[total_idx.index(self.sequence_id) - 1],
			},
			"completed_qty",
		)

	if self.for_quantity + completed_qty + process_loss_qty > qty_to_manufacture:
		frappe.throw(
			f"Qty to Manufacture in current operation cannot be greater than\
				S {frappe.bold(qty_to_manufacture - (completed_qty + process_loss_qty))}."
		)
	
	if self.sequence_id == total_idx[-1]:
		self.last_qty = self.for_quantity