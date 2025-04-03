
import frappe
import calendar
from datetime import datetime,timedelta,date
from erpnext.selling.report.sales_analytics.sales_analytics import execute
from frappe.utils import getdate
import json


@frappe.whitelist()
def re_sales_yet(filters=None):
    if isinstance(filters, str):  
        try:
            filters = json.loads(filters)  
        except json.JSONDecodeError:
            return {"error": "Invalid filters format. Expected JSON string."}

    if not filters:
        filters = {}

    # Automatically set the current financial year
    today = date.today()
    financial_year_start = date(today.year, 4, 1)  
    financial_year_end = date(today.year + 1, 3, 31) if today.month >= 4 else date(today.year, 3, 31)

    # Extract filters with default values if missing
    from_date = filters.get("from_date", str(financial_year_start))
    to_date = filters.get("to_date", str(financial_year_end))
    company = filters.get("company", "RBD Engineers Pvt Ltd")

    # Convert date strings to actual date objects (for validation)
    try:
        from_date = getdate(from_date)
        to_date = getdate(to_date)
    except ValueError:
        return {"error": "Invalid date format. Expected YYYY-MM-DD."}

    report_filters = {
        "from_date": str(from_date),
        "to_date": str(to_date),
        "company": company,
        "value_quantity": filters.get("value_quantity", "Value"),
        "doc_type": filters.get("doc_type", "Sales Invoice"),  # Ensure doc type is specified
        "tree_type": filters.get("tree_type", "Customer"),  #  Include tree type (Customer, Item, etc.)
        "range": filters.get("range", "Monthly"),  #  Specify range (Weekly, Monthly, etc.)
    }   
   
    try:
        _, data, *_ = execute(report_filters)  # Extract only `data`
    except Exception as e:
        return {"error": f"Error executing Sales Analytics: {str(e)}"}
   
    total = 0
    if isinstance(data, list):  
        for row in data:
            if isinstance(row, dict):  
                total += float(row.get("total", 0) or 0)  # Safely convert to float

    return {
        "value": total,
        "fieldtype": "Float",
        "precision": 3,
        "route_options": report_filters,
        "route": ["query-report", "Sales Analytics"]
    }
    
    
@frappe.whitelist()
def rc_sales_yet(filters=None):
    if isinstance(filters, str):  
        try:
            filters = json.loads(filters)  
        except json.JSONDecodeError:
            return {"error": "Invalid filters format. Expected JSON string."}

    if not filters:
        filters = {}

    today = date.today()
    financial_year_start = date(today.year, 4, 1)  
    financial_year_end = date(today.year + 1, 3, 31) if today.month >= 4 else date(today.year, 3, 31)

    from_date = filters.get("from_date", str(financial_year_start))
    to_date = filters.get("to_date", str(financial_year_end))
    company = filters.get("company", "RBD Castech Pvt Ltd")

    try:
        from_date = getdate(from_date)
        to_date = getdate(to_date)
    except ValueError:
        return {"error": "Invalid date format. Expected YYYY-MM-DD."}

    report_filters = {
        "from_date": str(from_date),
        "to_date": str(to_date),
        "company": company,
        "value_quantity": filters.get("value_quantity", "Value"),
        "doc_type": filters.get("doc_type", "Sales Invoice"),  # Ensure doc type is specified
        "tree_type": filters.get("tree_type", "Customer"),  #  Include tree type (Customer, Item, etc.)
        "range": filters.get("range", "Monthly"),  #  Specify range (Weekly, Monthly, etc.)
    }   
   
    try:
        _, data, *_ = execute(report_filters)  # Extract only `data`
    except Exception as e:
        return {"error": f"Error executing Sales Analytics: {str(e)}"}
   
    total = 0
    if isinstance(data, list):  
        for row in data:
            if isinstance(row, dict):  
                total += float(row.get("total", 0) or 0)  # Safely convert to float

    return {
        "value": total,
        "fieldtype": "Float",
        "precision": 3,
        "route_options": report_filters,
        "route": ["query-report", "Sales Analytics"]
    }