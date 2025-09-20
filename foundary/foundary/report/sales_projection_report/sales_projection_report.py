# # Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
# # For license information, please see license.txt

# # import frappe

# import frappe
# from frappe.utils import flt
# from frappe.utils import getdate
# import calendar
# from frappe.utils import getdate, nowdate


# @frappe.whitelist()
# def get_current_fiscal_year():
#     from frappe.utils import nowdate, getdate
#     today = getdate(nowdate())
#     fiscal_year = frappe.get_all("Fiscal Year", 
#         filters={
#             "year_start_date": ["<=", today],
#             "year_end_date": [">=", today]
#         },
#         fields=["name"],
#         limit=1
#     )
#     return fiscal_year[0].name if fiscal_year else None

# def execute(filters=None):
#     columns = [
#         {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 180},
#         {"label": "Sales Order Amount", "fieldname": "sales_order_amount", "fieldtype": "Currency", "width": 150},
#         {"label": "Total Committed Amount", "fieldname": "committed_amount", "fieldtype": "Currency", "width": 180},
#         {"label": "Actual Amount", "fieldname": "actual_amount", "fieldtype": "Currency", "width": 150},
#         {"label": "Sales Order Qty", "fieldname": "sales_order_qty", "fieldtype": "Float", "width": 150},
#         {"label": "Total Committed Qty", "fieldname": "committed_qty", "fieldtype": "Float", "width": 180},
#         {"label": "Actual Qty", "fieldname": "actual_qty", "fieldtype": "Float", "width": 150},
#         {"label": "Difference Qty", "fieldname": "diff_qty", "fieldtype": "Float", "width": 150},
#         {"label": "Difference Amount", "fieldname": "diff_amount", "fieldtype": "Currency", "width": 180},
#         {"label": "Sales Order ID", "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "width": 180},

#     ]

#     data = []
#     projected_qty = 0
#     projected_amount = 0
    
#     sales_order_filters = {"docstatus": 1}    
#     month_name = filters.get("month")
    
    
#     if not filters.get("financial_year"):
#         filters["financial_year"] = get_current_fiscal_year()
    
#     fy = filters.get("financial_year")
#     fiscal_year_doc = frappe.get_doc("Fiscal Year", fy)
#     from_date = fiscal_year_doc.year_start_date
#     to_date = fiscal_year_doc.year_end_date
    
#     if month_name and fy:
#         # Get Fiscal Year start and end dates
#         fy_doc = frappe.get_doc("Fiscal Year", fy)
#         year_start = fy_doc.year_start_date

#         # Month number
#         month_number = {
#             "January": 1, "February": 2, "March": 3, "April": 4,
#             "May": 5, "June": 6, "July": 7, "August": 8,
#             "September": 9, "October": 10, "November": 11, "December": 12
#         }.get(month_name)

#         if not month_number:
#             frappe.throw("Invalid Month Selected")

#         # Compute the actual year for the selected month
#         base_year = year_start.year
#         if month_number < year_start.month:
#             base_year += 1

#         from_date = getdate(f"{base_year}-{month_number:02d}-01")
#         last_day = calendar.monthrange(base_year, month_number)[1]
#         to_date = getdate(f"{base_year}-{month_number:02d}-{last_day}")

#         # Use from_date and to_date in your filters
#         sales_order_filters = {
#             "delivery_date": ["between", [from_date, to_date]],
#             "docstatus": 1
#         }
    
#     if filters.get("company"):
#         sales_order_filters["company"] = filters["company"]
    
#     # If custom date range is given, use it
#     if filters.get("from_date") and filters.get("to_date"):
#         sales_order_filters["delivery_date"] = ["between", [filters["from_date"], filters["to_date"]]]
#     elif filters.get("from_date"):
#         sales_order_filters["delivery_date"] = [">=", filters["from_date"]]
#     elif filters.get("to_date"):
#         sales_order_filters["delivery_date"] = ["<=", filters["to_date"]]
#     else:
#         # Otherwise, use the fiscal year range as default
#         sales_order_filters["delivery_date"] = ["between", [from_date, to_date]]

#     sales_orders = frappe.db.get_all("Sales Order", filters=sales_order_filters, fields=[
#         "name", "customer", "base_total", "total_qty", "total_commited_amount_inr", "total_committed_amount","total_committed_qty"
#     ])
    


#     for so in sales_orders:
    
#         actuals = frappe.db.sql("""
#             SELECT
#                 SUM(si.total_qty) AS actual_qty,
#                 SUM(si.base_total) AS actual_amount
#             FROM `tabSales Invoice` si
#             WHERE si.name IN (
#                 SELECT DISTINCT parent
#                 FROM `tabSales Invoice Item`
#                 WHERE sales_order = %s
#             ) AND si.docstatus = 1
#         """, so.name, as_dict=True)[0]


#         actual_qty = flt(actuals.actual_qty)
#         actual_amount = flt(actuals.actual_amount)
        
#         committed_qty = flt(so.total_committed_qty)
#         committed_amount = flt(so.total_commited_amount_inr)

#         # Add to projected totals
#         # projected_qty += committed_qty
#         # projected_amount += committed_amount

#         data.append({
#             "customer": so.customer,
#             "sales_order_amount": so.base_total,
#             "committed_amount": so.total_commited_amount_inr,
#             "actual_amount": actual_amount,
#             "sales_order_qty": so.total_qty,
#             "committed_qty": so.total_committed_qty,
#             "actual_qty": actual_qty,
#             "diff_qty": committed_qty- actual_qty,
#             "diff_amount": committed_amount - actual_amount,
#             "sales_order": so.name
#         })
        
#     return columns, data


# # Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.utils import flt, getdate, nowdate
# import calendar


# @frappe.whitelist()
# def get_current_fiscal_year():
#     today = getdate(nowdate())
#     fiscal_year = frappe.get_all(
#         "Fiscal Year",
#         filters={
#             "year_start_date": ["<=", today],
#             "year_end_date": [">=", today]
#         },
#         fields=["name"],
#         limit=1
#     )
#     return fiscal_year[0].name if fiscal_year else None


# def execute(filters=None):
#     columns = [
#         {"label": "Sales Order ID", "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "width": 180},
#         {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 180},
#         {"label": "Sales Order Qty", "fieldname": "sales_order_qty", "fieldtype": "Float", "width": 150},
#         {"label": "Sales Order Amount", "fieldname": "sales_order_amount", "fieldtype": "Currency", "width": 150},
#         {"label": "Total Committed Qty", "fieldname": "committed_qty", "fieldtype": "Float", "width": 180},
#         {"label": "Total Committed Amount", "fieldname": "committed_amount", "fieldtype": "Currency", "width": 180},
#         {"label": "Actual Qty", "fieldname": "actual_qty", "fieldtype": "Float", "width": 150},
#         {"label": "Actual Amount", "fieldname": "actual_amount", "fieldtype": "Currency", "width": 150},
#         {"label": "Difference Qty", "fieldname": "diff_qty", "fieldtype": "Float", "width": 150},
#         {"label": "Difference Amount", "fieldname": "diff_amount", "fieldtype": "Currency", "width": 180},
        
#     ]

#     data = []
#     sales_order_filters = {"docstatus": 1}
#     month_name = filters.get("month")

#     # default fiscal year
#     if not filters.get("financial_year"):
#         filters["financial_year"] = get_current_fiscal_year()

#     fy = filters.get("financial_year")
#     fiscal_year_doc = frappe.get_doc("Fiscal Year", fy)
#     from_date = fiscal_year_doc.year_start_date
#     to_date = fiscal_year_doc.year_end_date

#     # If month filter is applied
#     if month_name and fy:
#         fy_doc = frappe.get_doc("Fiscal Year", fy)
#         year_start = fy_doc.year_start_date

#         month_number = {
#             "January": 1, "February": 2, "March": 3, "April": 4,
#             "May": 5, "June": 6, "July": 7, "August": 8,
#             "September": 9, "October": 10, "November": 11, "December": 12
#         }.get(month_name)

#         if not month_number:
#             frappe.throw("Invalid Month Selected")

#         base_year = year_start.year
#         if month_number < year_start.month:
#             base_year += 1

#         from_date = getdate(f"{base_year}-{month_number:02d}-01")
#         last_day = calendar.monthrange(base_year, month_number)[1]
#         to_date = getdate(f"{base_year}-{month_number:02d}-{last_day}")

#         sales_order_filters = {
#             "delivery_date": ["between", [from_date, to_date]],
#             "docstatus": 1
#         }

#     if filters.get("company"):
#         sales_order_filters["company"] = filters["company"]

#     # If custom date range is given
#     if filters.get("from_date") and filters.get("to_date"):
#         sales_order_filters["delivery_date"] = ["between", [filters["from_date"], filters["to_date"]]]
#     elif filters.get("from_date"):
#         sales_order_filters["delivery_date"] = [">=", filters["from_date"]]
#     elif filters.get("to_date"):
#         sales_order_filters["delivery_date"] = ["<=", filters["to_date"]]
#     else:
#         sales_order_filters["delivery_date"] = ["between", [from_date, to_date]]

#     # Fetch Sales Orders
#     sales_orders = frappe.db.get_all(
#         "Sales Order",
#         filters=sales_order_filters,
#         fields=[
#             "name", "customer", "base_total", "total_qty",
#             "total_commited_amount_inr", "total_committed_qty"
#         ]
#     )

#     for so in sales_orders:
#         actual_source = "Delivery Note"

#         # First try Delivery Notes
#         actuals = frappe.db.sql("""
#             SELECT
#                 SUM(dni.qty) AS actual_qty,
#                 SUM(dni.amount) AS actual_amount
#             FROM `tabDelivery Note Item` dni
#             JOIN `tabDelivery Note` dn ON dn.name = dni.parent
#             WHERE dni.against_sales_order = %s AND dn.docstatus = 1
#         """, so.name, as_dict=True)[0]

#         actual_qty = flt(actuals.actual_qty) if actuals.actual_qty else 0
#         actual_amount = flt(actuals.actual_amount) if actuals.actual_amount else 0

#         # If no DN data, fallback to Sales Invoice
#         if not actual_qty and not actual_amount:
#             actual_source = "Sales Invoice"
#             invoice_actuals = frappe.db.sql("""
#                 SELECT
#                     SUM(si.total_qty) AS actual_qty,
#                     SUM(si.base_total) AS actual_amount
#                 FROM `tabSales Invoice` si
#                 WHERE si.name IN (
#                     SELECT DISTINCT parent
#                     FROM `tabSales Invoice Item`
#                     WHERE sales_order = %s
#                 ) AND si.docstatus = 1
#             """, so.name, as_dict=True)[0]

#             actual_qty = flt(invoice_actuals.actual_qty)
#             actual_amount = flt(invoice_actuals.actual_amount)

#         committed_qty = flt(so.total_committed_qty)
#         committed_amount = flt(so.total_commited_amount_inr)

#         data.append({
#             "customer": so.customer,
#             "sales_order_amount": so.base_total,
#             "committed_amount": committed_amount,
#             "actual_amount": actual_amount,
#             "sales_order_qty": so.total_qty,
#             "committed_qty": committed_qty,
#             "actual_qty": actual_qty,
#             "diff_qty": committed_qty - actual_qty,
#             "diff_amount": committed_amount - actual_amount,
#             "actual_source": actual_source,
#             "sales_order": so.name
#         })

#     return columns, data


# # Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.utils import flt, getdate, nowdate
# import calendar


# @frappe.whitelist()
# def get_current_fiscal_year():
#     """
#     Returns the current fiscal year based on today's date.
#     """
#     today = getdate(nowdate())
#     fiscal_year = frappe.get_all(
#         "Fiscal Year",
#         filters={
#             "year_start_date": ["<=", today],
#             "year_end_date": [">=", today]
#         },
#         fields=["name"],
#         limit=1
#     )
#     return fiscal_year[0].name if fiscal_year else None


# def execute(filters=None):
#     """
#     Generates a Sales Projection Report showing committed vs. actual sales.
#     """
#     columns = [
#         {"label": "Sales Order ID", "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "width": 180},
#         {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 180},
#         {"label": "Sales Order Qty", "fieldname": "sales_order_qty", "fieldtype": "Float", "width": 150},
#         {"label": "Sales Order Amount", "fieldname": "sales_order_amount", "fieldtype": "Currency", "width": 150},
#         {"label": "Total Committed Qty", "fieldname": "committed_qty", "fieldtype": "Float", "width": 180},
#         {"label": "Total Committed Amount", "fieldname": "committed_amount", "fieldtype": "Currency", "width": 180},
#         {"label": "Actual Qty", "fieldname": "actual_qty", "fieldtype": "Float", "width": 150},
#         {"label": "Actual Amount", "fieldtype": "Currency", "width": 150},
#         {"label": "Difference Qty", "fieldname": "diff_qty", "fieldtype": "Float", "width": 150},
#         {"label": "Difference Amount", "fieldname": "diff_amount", "fieldtype": "Currency", "width": 180},
#     ]

#     data = []
    
#     # 1. Determine the date range based on filters
#     from_date = filters.get("from_date")
#     to_date = filters.get("to_date")
    
#     if not from_date or not to_date:
#         if not filters.get("financial_year"):
#             filters["financial_year"] = get_current_fiscal_year()

#         fy = filters.get("financial_year")
#         fiscal_year_doc = frappe.get_doc("Fiscal Year", fy)
#         from_date = fiscal_year_doc.year_start_date
#         to_date = fiscal_year_doc.year_end_date

#         if filters.get("month"):
#             month_name = filters.get("month")
#             month_number = {
#                 "January": 1, "February": 2, "March": 3, "April": 4,
#                 "May": 5, "June": 6, "July": 7, "August": 8,
#                 "September": 9, "October": 10, "November": 11, "December": 12
#             }.get(month_name)

#             if not month_number:
#                 frappe.throw("Invalid Month Selected")

#             base_year = fiscal_year_doc.year_start_date.year
#             if month_number < fiscal_year_doc.year_start_date.month:
#                 base_year += 1

#             from_date = getdate(f"{base_year}-{month_number:02d}-01")
#             last_day = calendar.monthrange(base_year, month_number)[1]
#             to_date = getdate(f"{base_year}-{month_number:02d}-{last_day}")

#     # 2. Fetch all 'actuals' data (qty and amount) grouped by Sales Order up to the `to_date` of the report
    
#     actuals_data = {}

#     # Query Delivery Notes up to the selected date
#     delivery_note_data = frappe.db.sql("""
#         SELECT
#             dni.against_sales_order,
#             SUM(dni.qty) AS actual_qty,
#             SUM(dni.amount) AS actual_amount
#         FROM `tabDelivery Note Item` dni
#         JOIN `tabDelivery Note` dn ON dn.name = dni.parent
#         WHERE dn.docstatus = 1 AND dn.posting_date <= %s
#         GROUP BY dni.against_sales_order
#     """, (to_date), as_dict=True)

#     for row in delivery_note_data:
#         so_name = row.get("against_sales_order")
#         if so_name:
#             if so_name not in actuals_data:
#                 actuals_data[so_name] = {"actual_qty": 0, "actual_amount": 0, "actual_source": "Delivery Note"}
#             actuals_data[so_name]["actual_qty"] += flt(row.actual_qty)
#             actuals_data[so_name]["actual_amount"] += flt(row.actual_amount)

#     # Query Sales Invoices (for cases where no DN exists)
#     sales_invoice_data = frappe.db.sql("""
#         SELECT
#             sii.sales_order,
#             SUM(sii.qty) AS actual_qty,
#             SUM(sii.amount) AS actual_amount
#         FROM `tabSales Invoice Item` sii
#         JOIN `tabSales Invoice` si ON si.name = sii.parent
#         WHERE si.docstatus = 1 AND si.posting_date <= %s
#         GROUP BY sii.sales_order
#     """, (to_date), as_dict=True)

#     for row in sales_invoice_data:
#         so_name = row.get("sales_order")
#         if so_name and so_name not in actuals_data:
#             # Only add if not already in DN data
#             actuals_data[so_name] = {
#                 "actual_qty": flt(row.actual_qty),
#                 "actual_amount": flt(row.actual_amount),
#                 "actual_source": "Sales Invoice"
#             }
#         elif so_name:
#              # Add to existing totals if DN for the same SO exists
#              actuals_data[so_name]["actual_qty"] += flt(row.actual_qty)
#              actuals_data[so_name]["actual_amount"] += flt(row.actual_amount)

#     # 3. Get the list of Sales Orders that had an actual delivery/invoice in the selected period
#     actuals_in_period = frappe.db.sql("""
#         SELECT DISTINCT against_sales_order AS name FROM `tabDelivery Note Item` dni
#         JOIN `tabDelivery Note` dn ON dn.name = dni.parent
#         WHERE dn.docstatus = 1 AND dn.posting_date BETWEEN %s AND %s
#         UNION
#         SELECT DISTINCT sales_order AS name FROM `tabSales Invoice Item` sii
#         JOIN `tabSales Invoice` si ON si.name = sii.parent
#         WHERE si.docstatus = 1 AND si.posting_date BETWEEN %s AND %s
#     """, (from_date, to_date, from_date, to_date), as_dict=True)
    
#     so_names_to_show = {row.name for row in actuals_in_period}

#     # 4. Fetch related Sales Order data and build the final report
#     if so_names_to_show:
#         so_filters = {"name": ["in", list(so_names_to_show)], "docstatus": 1}
#         if filters.get("company"):
#             so_filters["company"] = filters["company"]

#         sales_orders = frappe.get_all(
#             "Sales Order",
#             filters=so_filters,
#             fields=[
#                 "name", "customer", "base_total", "total_qty",
#                 "total_commited_amount_inr", "total_committed_qty"
#             ]
#         )

#         for so in sales_orders:
#             so_data = actuals_data.get(so.name)
#             if so_data:
#                 committed_qty = flt(so.total_committed_qty)
#                 committed_amount = flt(so.total_commited_amount_inr)
#                 actual_qty = so_data["actual_qty"]
#                 actual_amount = so_data["actual_amount"]

#                 data.append({
#                     "customer": so.customer,
#                     "sales_order_amount": so.base_total,
#                     "committed_amount": committed_amount,
#                     "actual_amount": actual_amount,
#                     "sales_order_qty": so.total_qty,
#                     "committed_qty": committed_qty,
#                     "actual_qty": actual_qty,
#                     "diff_qty": committed_qty - actual_qty,
#                     "diff_amount": committed_amount - actual_amount,
#                     "actual_source": so_data["actual_source"],
#                     "sales_order": so.name
#                 })

#     return columns, data

# Copyright (c) 2025, Finbyz Tech PVT LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt, getdate, nowdate
import calendar


@frappe.whitelist()
def get_current_fiscal_year():
    """
    Returns the current fiscal year based on today's date.
    """
    today = getdate(nowdate())
    fiscal_year = frappe.get_all(
        "Fiscal Year",
        filters={
            "year_start_date": ["<=", today],
            "year_end_date": [">=", today]
        },
        fields=["name"],
        limit=1
    )
    return fiscal_year[0].name if fiscal_year else None


def execute(filters=None):
    """
    Generates a Sales Projection Report showing committed vs. actual sales.
    """
    columns = [
        {"label": "Sales Order ID", "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "width": 180},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 180},
        {"label": "Sales Order Qty", "fieldname": "sales_order_qty", "fieldtype": "Float", "width": 150},
        {"label": "Sales Order Amount", "fieldname": "sales_order_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Total Committed Qty", "fieldname": "committed_qty", "fieldtype": "Float", "width": 180},
        {"label": "Total Committed Amount", "fieldname": "committed_amount", "fieldtype": "Currency", "width": 180},
        {"label": "Actual Qty", "fieldname": "actual_qty", "fieldtype": "Float", "width": 150},
        {"label": "Actual Amount", "fieldname": "actual_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Difference Qty", "fieldname": "diff_qty", "fieldtype": "Float", "width": 150},
        {"label": "Difference Amount", "fieldname": "diff_amount", "fieldtype": "Currency", "width": 180},
    ]

    data = []
    
    # 1. Determine the date range based on filters
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    
    if not from_date or not to_date:
        if not filters.get("financial_year"):
            filters["financial_year"] = get_current_fiscal_year()

        fy = filters.get("financial_year")
        fiscal_year_doc = frappe.get_doc("Fiscal Year", fy)
        from_date = fiscal_year_doc.year_start_date
        to_date = fiscal_year_doc.year_end_date

        if filters.get("month"):
            month_name = filters.get("month")
            month_number = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12
            }.get(month_name)

            if not month_number:
                frappe.throw("Invalid Month Selected")

            base_year = fiscal_year_doc.year_start_date.year
            if month_number < fiscal_year_doc.year_start_date.month:
                base_year += 1

            from_date = getdate(f"{base_year}-{month_number:02d}-01")
            last_day = calendar.monthrange(base_year, month_number)[1]
            to_date = getdate(f"{base_year}-{month_number:02d}-{last_day}")

    # 2. Fetch monthly 'actuals' data (qty and amount) grouped by Sales Order
    monthly_actuals_data = {}

    # Query Delivery Notes for the SELECTED MONTH only
    delivery_note_data = frappe.db.sql("""
        SELECT
            dni.against_sales_order,
            SUM(dni.qty) AS actual_qty,
            SUM(dni.amount) AS actual_amount
        FROM `tabDelivery Note Item` dni
        JOIN `tabDelivery Note` dn ON dn.name = dni.parent
        WHERE dn.docstatus = 1 AND dn.posting_date BETWEEN %s AND %s
        GROUP BY dni.against_sales_order
    """, (from_date, to_date), as_dict=True)

    for row in delivery_note_data:
        so_name = row.get("against_sales_order")
        if so_name:
            monthly_actuals_data[so_name] = {
                "actual_qty": flt(row.actual_qty), 
                "actual_amount": flt(row.actual_amount)
            }

    # Query Sales Invoices (for cases where no DN exists) for the SELECTED MONTH only
    sales_invoice_data = frappe.db.sql("""
        SELECT
            sii.sales_order,
            SUM(sii.qty) AS actual_qty,
            SUM(sii.amount) AS actual_amount
        FROM `tabSales Invoice Item` sii
        JOIN `tabSales Invoice` si ON si.name = sii.parent
        WHERE si.docstatus = 1 AND si.posting_date BETWEEN %s AND %s
        GROUP BY sii.sales_order
    """, (from_date, to_date), as_dict=True)

    for row in sales_invoice_data:
        so_name = row.get("sales_order")
        if so_name and so_name not in monthly_actuals_data:
            monthly_actuals_data[so_name] = {
                "actual_qty": flt(row.actual_qty), 
                "actual_amount": flt(row.actual_amount)
            }
        elif so_name:
             # Add to existing totals if DN for the same SO exists
             monthly_actuals_data[so_name]["actual_qty"] += flt(row.actual_qty)
             monthly_actuals_data[so_name]["actual_amount"] += flt(row.actual_amount)

    # 3. Fetch CUMULATIVE 'actuals' up to the `to_date` to calculate the progressive difference
    cumulative_actuals_data = {}

    cumulative_dn_data = frappe.db.sql("""
        SELECT
            dni.against_sales_order,
            SUM(dni.qty) AS actual_qty,
            SUM(dni.amount) AS actual_amount
        FROM `tabDelivery Note Item` dni
        JOIN `tabDelivery Note` dn ON dn.name = dni.parent
        WHERE dn.docstatus = 1 AND dn.posting_date <= %s
        GROUP BY dni.against_sales_order
    """, (to_date), as_dict=True)

    for row in cumulative_dn_data:
        so_name = row.get("against_sales_order")
        if so_name:
            if so_name not in cumulative_actuals_data:
                cumulative_actuals_data[so_name] = {"actual_qty": 0, "actual_amount": 0}
            cumulative_actuals_data[so_name]["actual_qty"] += flt(row.actual_qty)
            cumulative_actuals_data[so_name]["actual_amount"] += flt(row.actual_amount)

    cumulative_si_data = frappe.db.sql("""
        SELECT
            sii.sales_order,
            SUM(sii.qty) AS actual_qty,
            SUM(sii.amount) AS actual_amount
        FROM `tabSales Invoice Item` sii
        JOIN `tabSales Invoice` si ON si.name = sii.parent
        WHERE si.docstatus = 1 AND si.posting_date <= %s
        GROUP BY sii.sales_order
    """, (to_date), as_dict=True)

    for row in cumulative_si_data:
        so_name = row.get("sales_order")
        if so_name and so_name not in cumulative_actuals_data:
            cumulative_actuals_data[so_name] = {
                "actual_qty": flt(row.actual_qty), 
                "actual_amount": flt(row.actual_amount)
            }
        elif so_name:
             cumulative_actuals_data[so_name]["actual_qty"] += flt(row.actual_qty)
             cumulative_actuals_data[so_name]["actual_amount"] += flt(row.actual_amount)

    # 4. Build the final report data by combining monthly display with cumulative difference
    so_names_to_show = list(monthly_actuals_data.keys())

    if so_names_to_show:
        so_filters = {"name": ["in", so_names_to_show], "docstatus": 1}
        if filters.get("company"):
            so_filters["company"] = filters["company"]

        sales_orders = frappe.get_all(
            "Sales Order",
            filters=so_filters,
            fields=[
                "name", "customer", "base_total", "total_qty",
                "total_commited_amount_inr", "total_committed_qty"
            ]
        )

        for so in sales_orders:
            monthly_data = monthly_actuals_data.get(so.name)
            cumulative_data = cumulative_actuals_data.get(so.name)

            if monthly_data and cumulative_data:
                committed_qty = flt(so.total_committed_qty)
                committed_amount = flt(so.total_commited_amount_inr)
                
                # Actual Qty is the amount for the current month only
                actual_qty = monthly_data["actual_qty"]
                actual_amount = monthly_data["actual_amount"]

                # Difference Qty is calculated using the CUMULATIVE amount
                diff_qty = committed_qty - cumulative_data["actual_qty"]
                diff_amount = committed_amount - cumulative_data["actual_amount"]

                data.append({
                    "customer": so.customer,
                    "sales_order_amount": so.base_total,
                    "committed_amount": committed_amount,
                    "actual_amount": actual_amount,
                    "sales_order_qty": so.total_qty,
                    "committed_qty": committed_qty,
                    "actual_qty": actual_qty,
                    "diff_qty": diff_qty,
                    "diff_amount": diff_amount,
                    "sales_order": so.name
                })

    return columns, data

