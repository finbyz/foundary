import datetime
import json
from typing import Optional

import frappe
from frappe import _, bold
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.query_builder import Criterion
from frappe.query_builder.functions import IfNull, Max, Min
from frappe.utils import (
	add_days,
	add_to_date,
	cint,
	flt,
	get_datetime,
	get_link_to_form,
	get_time,
	getdate,
	time_diff,
	time_diff_in_hours,
	time_diff_in_seconds,
)

from erpnext.manufacturing.doctype.manufacturing_settings.manufacturing_settings import (
	get_mins_between_operations,
)
from erpnext.manufacturing.doctype.workstation_type.workstation_type import get_workstations
from erpnext.manufacturing.doctype.job_card.job_card import JobCard

class OverlapError(frappe.ValidationError):
	pass


class OperationMismatchError(frappe.ValidationError):
	pass


class OperationSequenceError(frappe.ValidationError):
	pass


class JobCardCancelError(frappe.ValidationError):
	pass


class JobCardOverTransferError(frappe.ValidationError):
	pass


class CustomJobCard(JobCard):
	def update_work_order_data(self, for_quantity, process_loss_qty, time_in_mins, wo):
		workstation_hour_rate = frappe.get_value("Workstation", self.workstation, "hour_rate")
		jc = frappe.qb.DocType("Job Card")
		jctl = frappe.qb.DocType("Job Card Time Log")

		time_data = (
			frappe.qb.from_(jc)
			.from_(jctl)
			.select(Min(jctl.from_time).as_("start_time"), Max(jctl.to_time).as_("end_time"))
			.where(
				(jctl.parent == jc.name)
				& (jc.work_order == self.work_order)
				& (jc.operation_id == self.operation_id)
				& (jc.docstatus == 1)
				& (IfNull(jc.is_corrective_job_card, 0) == 0)
			)
		).run(as_dict=True)

		for data in wo.operations:
			if data.get("name") == self.operation_id:
				data.completed_qty = for_quantity
				data.process_loss_qty = process_loss_qty
				data.actual_operation_time = time_in_mins
				data.actual_start_time = time_data[0].start_time if time_data else None
				data.actual_end_time = time_data[0].end_time if time_data else None
				if data.get("workstation") != self.workstation:
					# workstations can change in a job card
					data.workstation = self.workstation
					data.hour_rate = flt(workstation_hour_rate)

		# bom = frappe.get_doc("BOM", self.bom_no)
		# routing = frappe.get_doc("Routing", bom.routing) 
		operations = wo.operations
		
		sequence_id = 0

		if operations:
			sorted_operations = sorted(operations, key=lambda x: x.idx, reverse=True)
			last_operation = sorted_operations[0]

			row = frappe.db.sql(""" select count(*) from `tabWork Order Operation` where parent=%s""",self.work_order, as_dict=1)[0]['count(*)']
			sorted_operation = sorted(operations, key=lambda x: x.idx, reverse=True)
			if row != 1:
				second_last_operation = sorted_operation[1]
				if self.operation == last_operation.operation:
					last_completed_qty = last_operation.completed_qty
					pro_loss_qty = last_operation.process_loss_qty
					all_process_loss_qty = frappe.db.sql(""" select sum(process_loss_qty) from `tabJob Card` where work_order=%s and docstatus = 1""",self.work_order, as_dict=1)[0]['sum(process_loss_qty)']
					manufactured_qty = frappe.db.get_value("Work Order", self.work_order, "produced_qty")
					process_loss_qty = frappe.db.get_value("Work Order", self.work_order, "process_loss_qty")
					pending_finish = flt(last_completed_qty) + flt(all_process_loss_qty) - flt(manufactured_qty) - flt(process_loss_qty)
					
					
					second_completed_qty = second_last_operation.completed_qty if second_last_operation else last_operation.completed_qty
					# frappe.throw(str(last_completed_qty) + '-' + str(pro_loss_qty))
					com_loss_qty = flt(last_completed_qty + pro_loss_qty) - flt(self.total_completed_qty + self.process_loss_qty)
					qty = flt(second_completed_qty) - flt(com_loss_qty)
					if self.for_quantity > qty:
						frappe.throw("Qty to manufacture in current operation cannot be greater than qty completed {0} in previous operation {1}.".format(second_completed_qty, second_last_operation.operation) )
					wo.db_set("pending_finish", pending_finish)		

				if self.operation == second_last_operation.operation:
					# frappe.throw(str(second_last_operation.completed_qty))
					last_completed_qty = last_operation.completed_qty
					pro_loss_qty = last_operation.process_loss_qty
					all_process_loss_qty = frappe.db.sql(""" select sum(process_loss_qty) from `tabJob Card` where work_order=%s and docstatus = 1""",self.work_order, as_dict=1)[0]['sum(process_loss_qty)']
					manufactured_qty = frappe.db.get_value("Work Order", self.work_order, "produced_qty")
					process_loss_qty = frappe.db.get_value("Work Order", self.work_order, "process_loss_qty")
					pending_finish = flt(last_completed_qty) + flt(all_process_loss_qty) - flt(manufactured_qty) - flt(process_loss_qty)

					second_completed_qty = second_last_operation.completed_qty
					com_loss_qty = flt(last_completed_qty + pro_loss_qty) - flt(self.total_completed_qty + self.process_loss_qty)
					qty = flt(second_completed_qty) - flt(com_loss_qty)
					if self.for_quantity > qty:
						frappe.throw("Qty to manufacture in current operation cannot be greater than qty completed {0} in previous operation {1}.".format(second_completed_qty, second_last_operation.operation) )
					wo.db_set("pending_finish", pending_finish)		

			if row == 1:
				second_last_operation = sorted_operation[0] 
				if self.operation == last_operation.operation: 
					last_completed_qty = last_operation.completed_qty
					pro_loss_qty = last_operation.process_loss_qty
					all_process_loss_qty = frappe.db.sql(""" select sum(process_loss_qty) from `tabJob Card` where work_order=%s and docstatus = 1""",self.work_order, as_dict=1)[0]['sum(process_loss_qty)']
					manufactured_qty = frappe.db.get_value("Work Order", self.work_order, "produced_qty")
					process_loss_qty = frappe.db.get_value("Work Order", self.work_order, "process_loss_qty")
					frappe.db.set_value("Work Order", self.work_order, "process_loss_qty", all_process_loss_qty)

					pending_finish = flt(last_completed_qty) + flt(all_process_loss_qty) - flt(manufactured_qty) - flt(all_process_loss_qty)
					# frappe.throw(str(pending_finish))
					
					second_completed_qty = second_last_operation.completed_qty if second_last_operation else last_operation.completed_qty
					com_loss_qty = flt(last_completed_qty + pro_loss_qty) - flt(self.total_completed_qty + self.process_loss_qty)
					qty = flt(second_completed_qty) - flt(com_loss_qty)
					# if self.for_quantity > qty:
					# 	frappe.throw("Qty to manufacture in current operation cannot be greater than qty completed {0} in previous operation {1}.".format(second_completed_qty, second_last_operation.operation) )
					wo.db_set("pending_finish", pending_finish)		

				if self.operation == second_last_operation.operation:
					last_completed_qty = last_operation.completed_qty
					pro_loss_qty = last_operation.process_loss_qty
					all_process_loss_qty = frappe.db.sql(""" select sum(process_loss_qty) from `tabJob Card` where work_order=%s and docstatus = 1""",self.work_order, as_dict=1)[0]['sum(process_loss_qty)']
					manufactured_qty = frappe.db.get_value("Work Order", self.work_order, "produced_qty")
					process_loss_qty = frappe.db.get_value("Work Order", self.work_order, "process_loss_qty")
					pending_finish = flt(last_completed_qty) + flt(all_process_loss_qty) - flt(manufactured_qty) - flt(process_loss_qty)

					second_completed_qty = second_last_operation.completed_qty
					com_loss_qty = flt(last_completed_qty + pro_loss_qty) - flt(self.total_completed_qty + self.process_loss_qty)
					qty = flt(second_completed_qty) - flt(com_loss_qty)
					# if self.for_quantity > qty:
					# 	frappe.throw("Qty to manufacture in current operation cannot be greater than qty completed {0} in previous operation {1}.".format(second_completed_qty, second_last_operation.operation) )
					wo.db_set("pending_finish", pending_finish)		

		wo.flags.ignore_validate_update_after_submit = True
		wo.update_operation_status()
		wo.calculate_operating_cost()
		wo.set_actual_dates()
		wo.save()
