import json

import frappe
from dateutil.relativedelta import relativedelta
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.query_builder import Case
from frappe.query_builder.functions import Sum
from frappe.utils import (
	cint,
	date_diff,
	flt,
	get_datetime,
	get_link_to_form,
	getdate,
	nowdate,
	time_diff_in_hours,
)
from pypika import functions as fn

from erpnext.manufacturing.doctype.bom.bom import (
	get_bom_item_rate,
	get_bom_items_as_dict,
	validate_bom_no,
)
from erpnext.manufacturing.doctype.manufacturing_settings.manufacturing_settings import (
	get_mins_between_operations,
)
from erpnext.stock.doctype.batch.batch import make_batch
from erpnext.stock.doctype.item.item import get_item_defaults, validate_end_of_life
from erpnext.stock.doctype.serial_no.serial_no import (
	auto_make_serial_nos,
	clean_serial_no_string,
	get_auto_serial_nos,
	get_serial_nos,
)
from erpnext.stock.stock_balance import get_planned_qty, update_bin_qty
from erpnext.stock.utils import get_bin, get_latest_stock_qty, validate_warehouse_company
from erpnext.utilities.transaction_base import validate_uom_is_integer
from erpnext.manufacturing.doctype.work_order.work_order import WorkOrder

class OverProductionError(frappe.ValidationError):
	pass


class CapacityError(frappe.ValidationError):
	pass


class StockOverProductionError(frappe.ValidationError):
	pass


class OperationTooLongError(frappe.ValidationError):
	pass


class ItemHasVariantError(frappe.ValidationError):
	pass


class SerialNoQtyError(frappe.ValidationError):
	pass

class CustomWorkOrder(WorkOrder):
	def update_work_order_qty(self):
		"""Update **Manufactured Qty** and **Material Transferred for Qty** in Work Order
		based on Stock Entry"""

		allowance_percentage = flt(
			frappe.db.get_single_value("Manufacturing Settings", "overproduction_percentage_for_work_order")
		)

		for purpose, fieldname in (
			("Manufacture", "produced_qty"),
			("Material Transfer for Manufacture", "material_transferred_for_manufacturing"),
		):
			if (
				purpose == "Material Transfer for Manufacture"
				and self.operations
				and self.transfer_material_against == "Job Card"
			):
				continue

			qty = self.get_transferred_or_manufactured_qty(purpose)

			completed_qty = self.qty + (allowance_percentage / 100 * self.qty)
			if qty > completed_qty:
				frappe.throw(
					_("{0} ({1}) cannot be greater than planned quantity ({2}) in Work Order {3}").format(
						self.meta.get_label(fieldname), qty, completed_qty, self.name
					),
					StockOverProductionError,
				)

			self.db_set(fieldname, qty)
			self.set_process_loss_qty()

			# bom = frappe.get_doc("BOM", self.bom_no)
			# routing = frappe.get_doc("Routing", bom.routing) 
			operations = self.operations
		
			sequence_id = 0
			pending_finsih_qty = 0 

			if operations:
				sorted_operations = sorted(operations, key=lambda x: x.idx, reverse=True)
				last_operation = sorted_operations[0]
				sequence = last_operation.sequence_id
				sequence_id = sequence_id + sequence
				last_completed_qty = last_operation.completed_qty
				all_process_loss_qty = frappe.db.sql(""" select sum(process_loss_qty) from `tabJob Card` where work_order=%s and docstatus = 1""",self.name, as_dict=1)[0]['sum(process_loss_qty)']
				manufactured_qty = qty
				process_loss_qty = self.process_loss_qty
				pending_finsih = flt(last_completed_qty) + flt(all_process_loss_qty) - flt(manufactured_qty) - flt(process_loss_qty)
				pending_finsih_qty = pending_finsih_qty + pending_finsih
				
				# frappe.msgprint(str(pending_finsih_qty) + '-' + str(last_completed_qty) + '-' + str(all_process_loss_qty) + '-' + str(manufactured_qty) + '-' + str(process_loss_qty))
			
			
		
		
				# frappe.throw(str(manufactured_qty))
				# frappe.throw(str(qty) + '-' + str(self.process_loss_qty))
			
			

			from erpnext.selling.doctype.sales_order.sales_order import update_produced_qty_in_so_item

			if self.sales_order and self.sales_order_item:
				update_produced_qty_in_so_item(self.sales_order, self.sales_order_item)
		
		self.db_set("pending_finish", pending_finsih_qty)
		pending = flt(self.pending_finish) - flt(self.produced_qty)
		self.db_set("pending_finish", pending)

		if self.production_plan:
			self.set_produced_qty_for_sub_assembly_item()
			self.update_production_plan_status()
