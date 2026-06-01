import frappe
from frappe import _
from foundary.foundary.doc_events.work_order import update_work_order_pending_finish_qty
from frappe.query_builder.functions import Sum
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry
from frappe.utils import (cint,flt)
import erpnext
from erpnext.stock.stock_ledger import get_valuation_rate

def validate(self,method):
	# update_additional_cost(self)
	pass

def on_submit(self, method):
	if self.work_order:
		work_order = frappe.get_doc("Work Order", self.work_order)
		pending_finish = update_work_order_pending_finish_qty(work_order)
		work_order.db_set("pending_finish", pending_finish)

def update_additional_cost(self):
	if self.purpose == "Manufacture" and self.bom_no:
		bom = frappe.get_doc("BOM",self.bom_no)
		abbr = frappe.db.get_value("Company",self.company,'abbr')
		
		if self.is_new() and not self.amended_from:
			if bom.additional_cost:
				for d in bom.additional_cost:	
					self.append('additional_costs', {
						'expense_account': 'Expenses Included In Valuation - {}'.format(abbr),
						'description': d.description,
						'qty': flt(self.fg_completed_qty),
						'rate': abs(d.rate),
						'amount':  abs(d.rate)* flt(self.fg_completed_qty),
						'base_amount':  abs(d.rate)* flt(self.fg_completed_qty)
					})
		else:
			for row in self.additional_costs:
				if bom.additional_cost:
					for d in bom.additional_cost:
						if row.description == d.description:
							row.rate = abs(d.rate)
							row.qty = flt(self.fg_completed_qty)
							if row.rate and row.qty:
								row.amount = abs(d.rate)* flt(self.fg_completed_qty)
								row.base_amount = abs(d.rate)*flt(self.fg_completed_qty)
		self.db_set('total_additional_costs',sum([row.amount for row in self.additional_costs]))



class FinishedGoodError(frappe.ValidationError):
	pass
		
class FinishedGoodError(frappe.ValidationError):
	pass



class CustomStockEntry(StockEntry):
	def before_validate(self):
		if self.stock_entry_type == "Manufacture" and self.bom_no:
			self.update_valuation_of_scrap_quantity()
	
	def update_valuation_of_scrap_quantity(self):
		finished_item = frappe.db.get_value("BOM", self.bom_no, "item")
		for row in self.items:
			if row.item_code == finished_item and row.item_code:
				row.allow_zero_valuation_rate = 0
		
		self.calculate_rate_and_amount()

	def check_if_operations_completed(self):
			"""Check if Time Sheets are completed against before manufacturing to capture operating costs."""
			prod_order = frappe.get_doc("Work Order", self.work_order)
			allowance_percentage = flt(
				frappe.db.get_single_value("Manufacturing Settings", "overproduction_percentage_for_work_order")
			)
			for d in prod_order.get("operations"):
				total_completed_qty = flt(self.fg_completed_qty) + flt(prod_order.produced_qty)
				completed_qty = (
					d.completed_qty + d.process_loss_qty + (allowance_percentage / 100 * d.completed_qty)
				)
				prev_completed_qty = d.completed_qty
				if (prev_completed_qty == 0 and total_completed_qty > flt(completed_qty)) \
					or (prev_completed_qty > 0 and prev_completed_qty > flt(completed_qty)):
					job_card = frappe.db.get_value("Job Card", {"operation_id": d.name}, "name")
					if not job_card:
						frappe.throw(
							_("Work Order {0}: Job Card not found for the operation {1}").format(
								self.work_order, d.operation
							)
						)

					work_order_link = frappe.utils.get_link_to_form("Work Order", self.work_order)
					job_card_link = frappe.utils.get_link_to_form("Job Card", job_card)
					frappe.throw(
						_(
							"Row #{0}: Operation {1} is not completed for {2} qty of finished goods in Work Order {3}. Please update operation status via Job Card {4}."
						).format(
							d.idx,
							frappe.bold(d.operation),
							frappe.bold(total_completed_qty),
							work_order_link,
							job_card_link,
						),
						OperationsNotCompleteError,
					)


	def set_process_loss_qty(self):
			if self.purpose not in ("Manufacture", "Repack"):
				return

			precision = self.precision("process_loss_qty")
			if self.work_order:
				data = frappe.get_all(
					"Work Order Operation",
					filters={"parent": self.work_order},
					fields=[{"SUM": "process_loss_qty", "as": "process_loss_qty"}],
				)

				finish_data = frappe.get_all(
					"Stock Entry",
					filters={
						"purpose": "Manufacture",
						"work_order": self.work_order,
						"docstatus": 1,
					},
					fields=[{"SUM": "process_loss_qty", "as": "process_loss_qty"}],
				)

				if data and data[0].process_loss_qty is not None:
					process_loss_qty = flt(data[0].process_loss_qty) - flt(finish_data[0].process_loss_qty)
					if flt(self.process_loss_qty, precision) != flt(process_loss_qty, precision):
						self.process_loss_qty = flt(process_loss_qty, precision)

						frappe.msgprint(
							_("The Process Loss Qty has reset as per job cards Process Loss Qty"), alert=True
						)

			if not self.process_loss_percentage and not self.process_loss_qty:
				self.process_loss_percentage = frappe.get_cached_value(
					"BOM", self.bom_no, "process_loss_percentage"
				)

			if self.process_loss_percentage and not self.process_loss_qty:
				self.process_loss_qty = flt(
					(flt(self.fg_completed_qty) * flt(self.process_loss_percentage)) / 100
				)
			elif self.process_loss_qty and not self.process_loss_percentage:
				self.process_loss_percentage = flt(
					(flt(self.process_loss_qty) / flt(self.fg_completed_qty)) * 100
				)

	def get_scrap_items_from_job_card(self):
			if not self.pro_doc:
				self.set_work_order_details()

			if not self.pro_doc.operations:
				return []

			job_card = frappe.qb.DocType("Job Card")
			job_card_scrap_item = frappe.qb.DocType("Job Card Scrap Item")

			scrap_items = (
				frappe.qb.from_(job_card)
				.select(
					Sum(job_card_scrap_item.stock_qty).as_("stock_qty"),
					job_card_scrap_item.item_code,
					job_card_scrap_item.item_name,
					job_card_scrap_item.description,
					job_card_scrap_item.stock_uom,
				)
				.join(job_card_scrap_item)
				.on(job_card_scrap_item.parent == job_card.name)
				.where(
					(job_card_scrap_item.item_code.isnotnull())
					& (job_card.work_order == self.work_order)
					& (job_card.docstatus == 1)
				)
				.groupby(job_card_scrap_item.item_code)
			).run(as_dict=1)

			pending_qty = flt(self.get_completed_job_card_qty()) - flt(self.pro_doc.produced_qty)

			used_scrap_items = self.get_used_scrap_items()
			for row in scrap_items:
				row.stock_qty -= flt(used_scrap_items.get(row.item_code))
				# row.stock_qty = (row.stock_qty) * flt(self.fg_completed_qty) / flt(pending_qty)

				if used_scrap_items.get(row.item_code):
					used_scrap_items[row.item_code] -= row.stock_qty

				if cint(frappe.get_cached_value("UOM", row.stock_uom, "must_be_whole_number")):
					row.stock_qty = frappe.utils.ceil(row.stock_qty)

			return scrap_items
	
	def set_basic_rate(self, reset_outgoing_rate=True, raise_error_if_no_rate=True):
		"""
		Set rate for outgoing, scrapped and finished items
		"""
		# Set rate for outgoing items
		finished_item = frappe.db.get_value("BOM", self.bom_no, "item")
		outgoing_items_cost = self.set_rate_for_outgoing_items(reset_outgoing_rate, raise_error_if_no_rate)
		finished_item_qty = sum(d.transfer_qty for d in self.items if (d.is_finished_item or (d.item_code == finished_item)))

		items = []
		# Set basic rate for incoming items
		for d in self.get("items"):
			if d.s_warehouse or d.set_basic_rate_manually:
				continue

			if d.allow_zero_valuation_rate:
				d.basic_rate = 0.0
				items.append(d.item_code)

			elif d.is_finished_item or (d.item_code == finished_item):
				if self.purpose == "Manufacture":
					d.basic_rate = self.get_basic_rate_for_manufactured_item(
						finished_item_qty, outgoing_items_cost
					)
				elif self.purpose == "Repack":
					d.basic_rate = self.get_basic_rate_for_repacked_items(d.transfer_qty, outgoing_items_cost)

			if not d.basic_rate and not d.allow_zero_valuation_rate:
				if self.is_new():
					raise_error_if_no_rate = False

				d.basic_rate = get_valuation_rate(
					d.item_code,
					d.t_warehouse,
					self.doctype,
					self.name,
					d.allow_zero_valuation_rate,
					currency=erpnext.get_company_currency(self.company),
					company=self.company,
					raise_error_if_no_rate=raise_error_if_no_rate,
					batch_no=d.batch_no,
					serial_and_batch_bundle=d.serial_and_batch_bundle,
				)

			# do not round off basic rate to avoid precision loss
			d.basic_rate = flt(d.basic_rate)
			d.basic_amount = flt(flt(d.transfer_qty) * flt(d.basic_rate), d.precision("basic_amount"))

		if items:
			message = ""

			if len(items) > 1:
				message = _(
					"Items rate has been updated to zero as Allow Zero Valuation Rate is checked for the following items: {0}"
				).format(", ".join(frappe.bold(item) for item in items))
			else:
				message = _(
					"Item rate has been updated to zero as Allow Zero Valuation Rate is checked for item {0}"
				).format(frappe.bold(items[0]))

			frappe.msgprint(message, alert=True)
	
	def get_basic_rate_for_manufactured_item(self, finished_item_qty, outgoing_items_cost=0) -> float:
		finished_item = frappe.db.get_value("BOM", self.bom_no, "item")
		settings = frappe.get_single("Manufacturing Settings")
		scrap_items_cost = sum([flt(d.basic_amount) for d in self.get("items") if d.item_code != finished_item])

		if settings.material_consumption:
			if settings.get_rm_cost_from_consumption_entry and self.work_order:
				# Validate only if Material Consumption Entry exists for the Work Order.
				if frappe.db.exists(
					"Stock Entry",
					{
						"docstatus": 1,
						"work_order": self.work_order,
						"purpose": "Material Consumption for Manufacture",
					},
				):
					for item in self.items:
						if not item.is_finished_item :
							label = frappe.get_meta(settings.doctype).get_label(
								"get_rm_cost_from_consumption_entry"
							)
							frappe.throw(
								_(
									"Row {0}: As {1} is enabled, raw materials cannot be added to {2} entry. Use {3} entry to consume raw materials."
								).format(
									item.idx,
									frappe.bold(label),
									frappe.bold(_("Manufacture")),
									frappe.bold(_("Material Consumption for Manufacture")),
								)
							)

					if frappe.db.exists(
						"Stock Entry",
						{"docstatus": 1, "work_order": self.work_order, "purpose": "Manufacture"},
					):
						frappe.throw(
							_("Only one {0} entry can be created against the Work Order {1}").format(
								frappe.bold(_("Manufacture")), frappe.bold(self.work_order)
							)
						)

					SE = frappe.qb.DocType("Stock Entry")
					SE_ITEM = frappe.qb.DocType("Stock Entry Detail")

					outgoing_items_cost = (
						frappe.qb.from_(SE)
						.left_join(SE_ITEM)
						.on(SE.name == SE_ITEM.parent)
						.select(Sum(SE_ITEM.valuation_rate * SE_ITEM.transfer_qty))
						.where(
							(SE.docstatus == 1)
							& (SE.work_order == self.work_order)
							& (SE.purpose == "Material Consumption for Manufacture")
						)
					).run()[0][0] or 0

			elif not outgoing_items_cost:
				bom_items = self.get_bom_raw_materials(finished_item_qty)
				outgoing_items_cost = sum([flt(row.qty) * flt(row.rate) for row in bom_items.values()])

		return flt((outgoing_items_cost - scrap_items_cost) / finished_item_qty)
