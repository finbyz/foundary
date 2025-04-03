import frappe
import json
from datetime import datetime, timedelta
from frappe.utils import flt

import frappe
import calendar
from datetime import datetime,timedelta
from foundary.foundary.report.rejection_analysis.rejection_analysis import execute
from foundary.foundary.report.rejection_analysis.rejection_analysis import execute

@frappe.whitelist()
def re_manufactured_qty_weighted(filters = None):
    today = datetime.today().date()
    from_date = today - timedelta(days=7)

    filters = {
        "from_date": str(from_date),
        "to_date": str(today)
    }
    
    conditions = ""

    if filters.get("from_date") and filters.get("to_date"):
        conditions += f" AND Date(jc.creation) BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'"
    
    # conditions += " "
        
    re_manufactured_qty_weighted = frappe.db.sql(f"""
        SELECT
            SUM(jc.total_completed_qty * i.weight_per_unit) AS rejected_qty_weight
        FROM 
            `tabJob Card` as jc
        JOIN
		    `tabItem` i ON jc.production_item = i.item_code
        WHERE
            jc.status = 'Completed'{conditions} AND jc.company = 'RBD Engineers Pvt Ltd' AND jc.docstatus = 1  AND i.name LIKE '%(F)%'
    """,as_dict=True)
    
    manufactured_qty_weight = 0.000
    # manufactured_qty_weight = re_manufactured_qty_weighted[0].rejected_qty_weight if re_manufactured_qty_weighted and re_manufactured_qty_weighted[0] is not None else 0.000
    manufactured_qty_weight = re_manufactured_qty_weighted[0].rejected_qty_weight if re_manufactured_qty_weighted and re_manufactured_qty_weighted[0] and re_manufactured_qty_weighted[0].rejected_qty_weight is not None else 0.000

    manufactured_qty_weight = round(manufactured_qty_weight,3) 
    return {
        "value": manufactured_qty_weight,
        "fieldtype": "Float",
        "precision": "3",
        "route_options": {
            "from_date": filters.get("from_date"),
            "to_date": filters.get("to_date"),
            "company": "RBD Engineers Pvt Ltd" 
        },
        "route": ["query-report", "Rejection Analysis"]
    }
    
@frappe.whitelist()
def rc_manufactured_qty_weighted(filters = None):
    today = datetime.today().date()
    from_date = today - timedelta(days=7)

    filters = {
        "from_date": str(from_date),
        "to_date": str(today)
    }
    
    conditions = ""

    if filters.get("from_date") and filters.get("to_date"):
        conditions += f" AND Date(jc.creation) BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'"
        
    rc_manufactured_qty_weighted = frappe.db.sql(f"""
        SELECT
            SUM(jc.total_completed_qty * i.weight_per_unit) AS rejected_qty_weight
        FROM 
            `tabJob Card` as jc
        JOIN
		    `tabItem` i ON jc.production_item = i.item_code
        WHERE
            jc.status = 'Completed'{conditions} AND jc.company = 'RBD Castech Pvt Ltd' AND jc.docstatus = 1  AND i.item_code LIKE '%(F)%'
    """,as_dict=True)
    manufactured_qty_weight = 0.000
    # manufactured_qty_weight = re_manufactured_qty_weighted[0].rejected_qty_weight if re_manufactured_qty_weighted and re_manufactured_qty_weighted[0] and re_manufactured_qty_weighted[0].rejected_qty_weight is not None else 0.000
    manufactured_qty_weight = rc_manufactured_qty_weighted[0].rejected_qty_weight if rc_manufactured_qty_weighted and rc_manufactured_qty_weighted[0] and rc_manufactured_qty_weighted[0].rejected_qty_weight is not None else 0.000
    manufactured_qty_weight = round(manufactured_qty_weight,3) 
    return {
        "value": manufactured_qty_weight,
        "fieldtype": "Float",
        "precision": "3",
        "route_options": {
            "from_date": filters.get("from_date"),
            "to_date": filters.get("to_date"),
            "company": 'RBD Castech Pvt Ltd'
        },
        "route": ["query-report", "Rejection Analysis"]
    }
    
