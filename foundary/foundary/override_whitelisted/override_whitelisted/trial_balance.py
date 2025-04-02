import frappe
import calendar
from datetime import datetime
from erpnext.accounts.report.trial_balance.trial_balance import execute

import frappe
import calendar
from datetime import datetime

def get_fiscal_year():
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    if current_month >= 4:  # Fiscal year starts in April
        return f"{current_year}-{current_year + 1}"
    else:
        return f"{current_year - 1}-{current_year}"


@frappe.whitelist()
def get_closing_balance_for_number_card(filters=None):
    # print(filters)
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
    fiscal_year = filters.get("fiscal_year", get_fiscal_year())
    print(fiscal_year)
    report_filters = frappe._dict({
        "company": company,
        "filter_based_on": "Date Range",
        "period_start_date": from_date,
        "period_end_date": to_date,
        "fiscal_year":fiscal_year ,  
        "periodicity": "Monthly",
    })

    # ✅ Fetch report data
    _, data = execute(report_filters)  # Extract only data from execute()
    # frappe.throw(str(data))
    closing_balance = 0
    # frappe.throw(str(data))
    
    if data and isinstance(data, list) and len(data) > 0:
        for row in data:
            if isinstance(row, dict) and row!= {} and row["account"] == 'Bank Accounts - REPL' and "closing_credit" in row.keys():
                closing_balance_credit = row['closing_credit']
            if isinstance(row, dict) and row!= {} and row["account"] == 'Bank Accounts - REPL' and "closing_debit" in row.keys():
                closing_balance_debit = row['closing_debit']
    closing_balance = closing_balance_credit - closing_balance_debit
    print(closing_balance)
    return {
        "value": closing_balance,
        "route_options": {
            "filter_based_on": "Date Range",
            "period_start_date": from_date,
            "period_end_date": to_date,
            "company": company,
            "fiscal_year": fiscal_year,
        },
        "route": ["query-report", "Trial Balance"]
    }
    
@frappe.whitelist()
def get_cc_hdfc_closing_balance(filters=None): 
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
    fiscal_year = filters.get("fiscal_year", get_fiscal_year())
    print(fiscal_year)
    report_filters = frappe._dict({
        "company": company,
        "filter_based_on": "Date Range",
        "period_start_date": from_date,
        "period_end_date": to_date,
        "fiscal_year":fiscal_year ,  
        "periodicity": "Monthly",
    })

    # ✅ Fetch report data
    _, data = execute(report_filters)  # Extract only data from execute()
    closing_balance = 0
    # frappe.throw(str(data))
    
    if data and isinstance(data, list) and len(data) > 0:
        for row in data:
            if isinstance(row, dict) and row!= {} and row["account"] == 'HDFC BANK A/C. (CC) : 50200002465012 - REPL' and "closing_credit" in row.keys():
                closing_balance_credit = row['closing_credit']
            if isinstance(row, dict) and row!= {} and row["account"] == 'HDFC BANK A/C. (CC) : 50200002465012 - REPL' and "closing_debit" in row.keys():
                closing_balance_debit = row['closing_debit']
    closing_balance = closing_balance_credit - closing_balance_debit
    print(closing_balance)
    return {
        "value": closing_balance,
        "route_options": {
            "filter_based_on": "Date Range",
            "period_start_date": from_date,
            "period_end_date": to_date,
            "company": company,
            "fiscal_year": fiscal_year,
        },
        "route": ["query-report", "Trial Balance"]
    }  
    
@frappe.whitelist()
def get_hdfc_closing_balance(filters=None): 
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
    fiscal_year = filters.get("fiscal_year", get_fiscal_year())
    print(fiscal_year)
    report_filters = frappe._dict({
        "company": company,
        "filter_based_on": "Date Range",
        "period_start_date": from_date,
        "period_end_date": to_date,
        "fiscal_year":fiscal_year ,  
        "periodicity": "Monthly",
    })

    # ✅ Fetch report data
    _, data = execute(report_filters)  # Extract only data from execute()
    closing_balance = 0
    # frappe.throw(str(data))
    
    if data and isinstance(data, list) and len(data) > 0:
        for row in data:
            if isinstance(row, dict) and row!= {} and row["account"] == 'HDFC BANK A/C. : 50200001671032 - REPL' and "closing_credit" in row.keys():
                closing_balance_credit = row['closing_credit']
            if isinstance(row, dict) and row!= {} and row["account"] == 'HDFC BANK A/C. : 50200001671032 - REPL' and "closing_debit" in row.keys():
                closing_balance_debit = row['closing_debit']
    closing_balance = closing_balance_credit - closing_balance_debit
    print(closing_balance)
    return {
        "value": closing_balance,
        "route_options": {
            "filter_based_on": "Date Range",
            "period_start_date": from_date,
            "period_end_date": to_date,
            "company": company,
            "fiscal_year": fiscal_year,
        },
        "route": ["query-report", "Trial Balance"]
    }     
    
@frappe.whitelist()
def get_hdfc_closing_balance_EEFC(filters=None): 
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
    fiscal_year = filters.get("fiscal_year", get_fiscal_year())
    print(fiscal_year)
    report_filters = frappe._dict({
        "company": company,
        "filter_based_on": "Date Range",
        "period_start_date": from_date,
        "period_end_date": to_date,
        "fiscal_year":fiscal_year ,  
        "periodicity": "Monthly",
    })

    # ✅ Fetch report data
    _, data = execute(report_filters)  # Extract only data from execute()
    closing_balance = 0
    # frappe.throw(str(data))
    
    if data and isinstance(data, list) and len(data) > 0:
        for row in data:
            if isinstance(row, dict) and row!= {} and row["account"] == 'Hdfc Bank EEFC A/c: 50200003907023 - REPL' and "closing_credit" in row.keys():
                closing_balance_credit = row['closing_credit']
            if isinstance(row, dict) and row!= {} and row["account"] == 'Hdfc Bank EEFC A/c: 50200003907023 - REPL' and "closing_debit" in row.keys():
                closing_balance_debit = row['closing_debit']
    closing_balance = closing_balance_credit - closing_balance_debit
    print(closing_balance)
    return {
        "value": closing_balance,
        "route_options": {
            "filter_based_on": "Date Range",
            "period_start_date": from_date,
            "period_end_date": to_date,
            "company": company,
            "fiscal_year": fiscal_year,
        },
        "route": ["query-report", "Trial Balance"]
    }     
    