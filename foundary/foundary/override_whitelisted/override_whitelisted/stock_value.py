import frappe
import calendar
from datetime import datetime
from erpnext.stock.report.stock_balance.stock_balance import execute

@frappe.whitelist()
def rc_stock_value(filters=None): 
    if filters and isinstance(filters, str):
        filters = frappe.parse_json(filters)
    if not isinstance(filters, dict):
        filters = {}

    today = datetime.today()
    first_day = today.replace(day=1)
    last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])

    from_date = filters.get("from_date") or first_day.strftime("%Y-%m-%d")
    to_date = filters.get("to_date") or last_day.strftime("%Y-%m-%d")

    if not from_date or not to_date:
        frappe.throw("From Date and To Date are mandatory.")

    company = filters.get("company", "RBD Castech Pvt Ltd")

    report_filters = frappe._dict({
        "company": company,
        "from_date": from_date,  
        "to_date": to_date,      
        "periodicity": "Monthly",
    })

    _, data = execute(report_filters)  

    Total = sum(row.get("bal_val", 0) for row in data if isinstance(row, dict))
    # frappe.throw(str(Total))
    return {
        "value": Total,
        "route_options": {
            "from_date": from_date,
            "to_date": to_date,
            "company": company,
        },
        "route": ["query-report", "Stock Balance"]  #  Correct route format
    }
    

@frappe.whitelist()
def re_stock_value(filters=None): 
    if filters and isinstance(filters, str):
        filters = frappe.parse_json(filters)
    if not isinstance(filters, dict):
        filters = {}

    today = datetime.today()
    first_day = today.replace(day=1)
    last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])

    from_date = filters.get("from_date") or first_day.strftime("%Y-%m-%d")
    to_date = filters.get("to_date") or last_day.strftime("%Y-%m-%d")

    if not from_date or not to_date:
        frappe.throw("From Date and To Date are mandatory.")

    company = filters.get("company", "RBD Engineers Pvt Ltd")

    report_filters = frappe._dict({
        "company": company,
        "from_date": from_date,  
        "to_date": to_date,      
        "periodicity": "Monthly",
    })

    _, data = execute(report_filters)  

    Total = sum(row.get("bal_val", 0) for row in data if isinstance(row, dict))
    # frappe.throw(str(Total))
    return {
        "value": Total,
        "route_options": {
            "from_date": from_date,
            "to_date": to_date,
            "company": company,
        },
        "route": ["query-report", "Stock Balance"]  #  Correct route format
    }