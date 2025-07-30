# Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe.utils import flt
from frappe.utils import getdate
import calendar

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
    year = filters.get("year")

    if month_name and year:
        try:
            month_number = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12
            }[month_name]

            year = int(year)
            from_date = getdate(f"{year}-{month_number:02d}-01")
            last_day = calendar.monthrange(year, month_number)[1]
            to_date = getdate(f"{year}-{month_number:02d}-{last_day}")

            sales_order_filters["delivery_date"] = ["between", [from_date, to_date]]
        except KeyError:
            frappe.throw(f"Invalid month: {month_name}")
        except ValueError:
            frappe.throw("Invalid year format")
    
    if filters.get("company"):
        sales_order_filters["company"] = filters["company"]
    
    if filters.get("from_date") and filters.get("to_date"):
        sales_order_filters["delivery_date"] = ["between", [filters["from_date"], filters["to_date"]]]
    elif filters.get("from_date"):
        sales_order_filters["delivery_date"] = [">=", filters["from_date"]]
    elif filters.get("to_date"):
        sales_order_filters["delivery_date"] = ["<=", filters["to_date"]]

    sales_orders = frappe.db.get_all("Sales Order", filters=sales_order_filters, fields=[
        "name", "customer", "base_total", "total_qty", "total_commited_amount_inr", "total_committed_amount","total_committed_qty"
    ])
    


    for so in sales_orders:
        actuals = frappe.db.sql("""
            SELECT
                SUM(sii.qty) AS actual_qty,
                SUM(si.base_total) AS actual_amount
            FROM
                `tabSales Invoice Item` sii
            INNER JOIN `tabSales Invoice` si ON si.name = sii.parent
            WHERE sii.sales_order = %s AND si.docstatus = 1
        """, so.name, as_dict=True)[0]

        actual_qty = flt(actuals.actual_qty)
        actual_amount = flt(actuals.actual_amount)
        
        committed_qty = flt(so.total_committed_qty)
        committed_amount = flt(so.total_committed_amount)

        # Add to projected totals
        projected_qty += committed_qty
        projected_amount += committed_amount

        data.append({
            "customer": so.customer,
            "sales_order_amount": so.base_total,
            "committed_amount": so.total_commited_amount_inr,
            "actual_amount": actual_amount,
            "sales_order_qty": so.total_qty,
            "committed_qty": so.total_committed_qty,
            "actual_qty": actual_qty,
            "diff_qty": flt(so.total_committed_qty) - actual_qty,
            "diff_amount": flt(so.total_committed_amount) - actual_amount,
            "sales_order": so.name
        })
        

    data.append({
        "customer": "Projected Qty",
        "committed_qty": projected_qty
    })

    data.append({
        "customer": "Projected Amount",
        "committed_amount": projected_amount
    })

    return columns, data
