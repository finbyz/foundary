# Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe.utils import flt
from frappe.utils import getdate
import calendar
from frappe.utils import getdate, nowdate


@frappe.whitelist()
def get_current_fiscal_year():
    from frappe.utils import nowdate, getdate
    today = getdate(nowdate())
    fiscal_year = frappe.get_all("Fiscal Year", 
        filters={
            "year_start_date": ["<=", today],
            "year_end_date": [">=", today]
        },
        fields=["name"],
        limit=1
    )
    return fiscal_year[0].name if fiscal_year else None

def execute(filters=None):
    columns = [
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 180},
        {"label": "Sales Order Amount", "fieldname": "sales_order_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Total Committed Amount", "fieldname": "committed_amount", "fieldtype": "Currency", "width": 180},
        {"label": "Actual Amount", "fieldname": "actual_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Sales Order Qty", "fieldname": "sales_order_qty", "fieldtype": "Float", "width": 150},
        {"label": "Total Committed Qty", "fieldname": "committed_qty", "fieldtype": "Float", "width": 180},
        {"label": "Actual Qty", "fieldname": "actual_qty", "fieldtype": "Float", "width": 150},
        {"label": "Difference Qty", "fieldname": "diff_qty", "fieldtype": "Float", "width": 150},
        {"label": "Difference Amount", "fieldname": "diff_amount", "fieldtype": "Currency", "width": 180},
        {"label": "Sales Order ID", "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "width": 180},

    ]

    data = []
    projected_qty = 0
    projected_amount = 0
    
    sales_order_filters = {"docstatus": 1}    
    month_name = filters.get("month")
    
    
    if not filters.get("financial_year"):
        filters["financial_year"] = get_current_fiscal_year()
    
    fy = filters.get("financial_year")
    fiscal_year_doc = frappe.get_doc("Fiscal Year", fy)
    from_date = fiscal_year_doc.year_start_date
    to_date = fiscal_year_doc.year_end_date
    
    if month_name and fy:
        # Get Fiscal Year start and end dates
        fy_doc = frappe.get_doc("Fiscal Year", fy)
        year_start = fy_doc.year_start_date

        # Month number
        month_number = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }.get(month_name)

        if not month_number:
            frappe.throw("Invalid Month Selected")

        # Compute the actual year for the selected month
        base_year = year_start.year
        if month_number < year_start.month:
            base_year += 1

        from_date = getdate(f"{base_year}-{month_number:02d}-01")
        last_day = calendar.monthrange(base_year, month_number)[1]
        to_date = getdate(f"{base_year}-{month_number:02d}-{last_day}")

        # Use from_date and to_date in your filters
        sales_order_filters = {
            "delivery_date": ["between", [from_date, to_date]],
            "docstatus": 1
        }
    
    if filters.get("company"):
        sales_order_filters["company"] = filters["company"]
    
    # If custom date range is given, use it
    if filters.get("from_date") and filters.get("to_date"):
        sales_order_filters["delivery_date"] = ["between", [filters["from_date"], filters["to_date"]]]
    elif filters.get("from_date"):
        sales_order_filters["delivery_date"] = [">=", filters["from_date"]]
    elif filters.get("to_date"):
        sales_order_filters["delivery_date"] = ["<=", filters["to_date"]]
    else:
        # Otherwise, use the fiscal year range as default
        sales_order_filters["delivery_date"] = ["between", [from_date, to_date]]

    sales_orders = frappe.db.get_all("Sales Order", filters=sales_order_filters, fields=[
        "name", "customer", "base_total", "total_qty", "total_commited_amount_inr", "total_committed_amount","total_committed_qty"
    ])
    


    for so in sales_orders:
    
        actuals = frappe.db.sql("""
            SELECT
                SUM(si.total_qty) AS actual_qty,
                SUM(si.base_total) AS actual_amount
            FROM `tabSales Invoice` si
            WHERE si.name IN (
                SELECT DISTINCT parent
                FROM `tabSales Invoice Item`
                WHERE sales_order = %s
            ) AND si.docstatus = 1
        """, so.name, as_dict=True)[0]


        actual_qty = flt(actuals.actual_qty)
        actual_amount = flt(actuals.actual_amount)
        
        committed_qty = flt(so.total_committed_qty)
        committed_amount = flt(so.total_commited_amount_inr)

        # Add to projected totals
        # projected_qty += committed_qty
        # projected_amount += committed_amount

        data.append({
            "customer": so.customer,
            "sales_order_amount": so.base_total,
            "committed_amount": so.total_commited_amount_inr,
            "actual_amount": actual_amount,
            "sales_order_qty": so.total_qty,
            "committed_qty": so.total_committed_qty,
            "actual_qty": actual_qty,
            "diff_qty": committed_qty- actual_qty,
            "diff_amount": committed_amount - actual_amount,
            "sales_order": so.name
        })
        
    return columns, data
