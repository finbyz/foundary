import frappe


def on_update(self, method):
	self.pending_finish = update_work_order_pending_finish_qty(self)
	

def on_update_after_submit(self, method):
	self.db_set("pending_finish", update_work_order_pending_finish_qty(self))


def update_work_order_pending_finish_qty(self):
	last_completed_qty = 0
	process_loss_qty = 0
	
	for row in self.operations:
		last_completed_qty = row.completed_qty
		process_loss_qty += row.process_loss_qty
	

	return flt(last_completed_qty) + flt(process_loss_qty) - flt(self.produced_qty) - flt(self.process_loss_qty)