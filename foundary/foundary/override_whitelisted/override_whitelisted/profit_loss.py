import frappe
from datetime import datetime
import calendar
from erpnext.accounts.report.profit_and_loss_statement.profit_and_loss_statement import execute

@frappe.whitelist()
def get_net_profit_for_number_card(filters=None):
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
        "filter_based_on": "Date Range",
        "period_start_date": from_date,
        "period_end_date": to_date,
        "periodicity": "Monthly",
    })

    # ✅ Fetch report data
    data = execute(report_filters)
    # ✅ Debugging

    net_profit = 0
    # frappe.throw(str(data))
    net_profit = (data[-1])
    
    return {
        "value": net_profit,
        "route_options": {
            "filter_based_on": "Date Range",
            "period_start_date": from_date,
            "period_end_date": to_date,
            "periodicity": "Monthly",
            "company": company,
            "fiscal_year": filters.get("fiscal_year"),
            "date_range": filters.get("date_range"),
        },
        "route": ["query-report", "Profit and Loss Statement"]
    }
    
@frappe.whitelist()
def rc_get_net_profit_for_number_card(filters=None):
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
        "filter_based_on": "Date Range",
        "period_start_date": from_date,
        "period_end_date": to_date,
        "periodicity": "Monthly",
    })

    # ✅ Fetch report data
    data = execute(report_filters)
    # ✅ Debugging

    net_profit = 0
    # frappe.throw(str(data))
    net_profit = (data[-1])
    
    return {
        "value": net_profit,
        "route_options": {
            "filter_based_on": "Date Range",
            "period_start_date": from_date,
            "period_end_date": to_date,
            "periodicity": "Monthly",
            "company": company,
            "fiscal_year": filters.get("fiscal_year"),
            "date_range": filters.get("date_range"),
        },
        "route": ["query-report", "Profit and Loss Statement"]
    }
    
@frappe.whitelist()
def re_get_gross_profit_for_number_card(filters=None):
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
        "filter_based_on": "Date Range",
        "period_start_date": from_date,
        "period_end_date": to_date,
        "periodicity": "Monthly",
    })

    # ✅ Fetch report data
    data = execute(report_filters)

    # ✅ Extract list from tuple if needed
    if isinstance(data, tuple) and len(data) > 0:
        data = data[1]  # Extract the list from the tuple

    # ✅ Initialize Variables
    direct_income = 0
    direct_expense = 0  

    # ✅ Iterate through the list of dictionaries
    if isinstance(data, list):  # Ensure it's a list before looping
        for row in data:
            # frappe.msgprint(str(row))
            if isinstance(row, dict) and row:  # Ensure row is a dictionary
                # frappe.msgprint(str(row.get("account")))
                if row.get("account") == "Direct Income - REPL" and "total" in row:
                    direct_income = row["total"]
                if row.get("account") == "Direct Expenses - REPL" and "total" in row:
                    direct_expense = row["total"]

    # ✅ Calculate Gross Profit
    print(direct_income, direct_expense)
    gross_profit = direct_income - direct_expense  

    return {
        "value": gross_profit,
        "route_options": {
            "filter_based_on": "Date Range",
            "period_start_date": from_date,
            "period_end_date": to_date,
            "periodicity": "Monthly",
            "company": company,
            "fiscal_year": filters.get("fiscal_year"),
            "date_range": filters.get("date_range"),
        },
        "route": ["query-report", "Profit and Loss Statement"]
    }


@frappe.whitelist()
def rc_get_gross_profit_for_number_card(filters=None):
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
        "filter_based_on": "Date Range",
        "period_start_date": from_date,
        "period_end_date": to_date,
        "periodicity": "Monthly",
    })

    # ✅ Fetch report data
    data = execute(report_filters)
    # ✅ Extract list from tuple if needed
    if isinstance(data, tuple) and len(data) > 0:
        data = data[1]  # Extract the list from the tuple

    # ✅ Initialize Variables
    direct_income = 0
    direct_expense = 0  

    # ✅ Iterate through the list of dictionaries
    if isinstance(data, list):  # Ensure it's a list before looping
        for row in data:
            if isinstance(row, dict) and row:  # Ensure row is a dictionary
                if row.get("account") == "Direct Income - RCPL" and "total" in row:
                    direct_income = row["total"]
                if row.get("account") == "Direct Expenses - RCPL" and "total" in row:
                    direct_expense = row["total"]

    # ✅ Calculate Gross Profit
    print(direct_income, direct_expense)
    gross_profit = direct_income - direct_expense  

    return {
        "value": gross_profit,
        "route_options": {
            "filter_based_on": "Date Range",
            "period_start_date": from_date,
            "period_end_date": to_date,
            "periodicity": "Monthly",
            "company": company,
            "fiscal_year": filters.get("fiscal_year"),
            "date_range": filters.get("date_range"),
        },
        "route": ["query-report", "Profit and Loss Statement"]
    }