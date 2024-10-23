import frappe
import json
from datetime import datetime, timedelta
from frappe.utils import flt

@frappe.whitelist()
def get_rejection_percentage_for_number_card(filters):
    today = datetime.today().date()
    from_date = today - timedelta(days=7)

    filters = {
        "from_date": str(from_date),
        "to_date": str(today)
    }
    
    conditions = ""

    if filters.get("from_date") and filters.get("to_date"):
        conditions += f" AND Date(jc.creation) BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'"
        
    total_rejected = frappe.db.sql(f"""
        SELECT
            SUM(jc.process_loss_qty) AS total_rejected
        FROM 
            `tabJob Card` as jc
        WHERE
            jc.status = 'Completed'{conditions} AND jc.company = 'RBD Engineers Pvt Ltd'
    """)

    total_to_manufacture = frappe.db.sql(f"""
    SELECT
        SUM(qty) AS total_to_manufacture
    FROM 
        `tabWork Order`
    WHERE
        creation BETWEEN '{filters.get("from_date")}' AND '{filters.get("to_date")}' 
        AND company = 'RBD Engineers Pvt Ltd'
        AND docstatus = 1
    """)
    
    total_rejected_value = total_rejected[0][0] if total_rejected and total_rejected[0][0] is not None else 0
    # frappe.throw(str(total_to_manufacture) + " " + str(total_rejected) + " " + str(rejection_percentage))
    total_to_manufacture_value = total_to_manufacture[0][0] if total_to_manufacture and total_to_manufacture[0][0] is not None else 0
    if total_to_manufacture_value != 0:
        rejection_percentage = round(((total_rejected_value / total_to_manufacture_value) * 100),3)
    else:
        rejection_percentage = 0
    return {
        "value": rejection_percentage,
        "fieldtype": "Percent",
       "route_options": {
            "from_date": filters.get("from_date"),
            "to_date": filters.get("to_date"),
            "company": "RBD Engineers Pvt Ltd" 
        },
        "route": ["query-report", "Rejection Analysis"]
    }


import frappe
import json

@frappe.whitelist()
def get_rejection_percentage_for_number_card_castech(filters):
    today = datetime.today().date()
    from_date = today - timedelta(days=7)

    filters = {
        "from_date": str(from_date),
        "to_date": str(today)
    }
    
    conditions = ""

    if filters.get("from_date") and filters.get("to_date"):
        conditions += f" AND Date(jc.creation) BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'"
        
    total_rejected = frappe.db.sql(f"""
        SELECT
            SUM(jc.process_loss_qty) AS total_rejected
        FROM 
            `tabJob Card` as jc
        WHERE
            jc.status = 'Completed'{conditions} AND jc.company = 'RBD Castech Pvt Ltd' AND jc.docstatus = 1
    """)

    total_to_manufacture = frappe.db.sql(f"""
    SELECT
        SUM(qty) AS total_to_manufacture
    FROM 
        `tabWork Order`
    WHERE
        creation BETWEEN '{filters.get("from_date")}' AND '{filters.get("to_date")}' 
        AND company = 'RBD Castech Pvt Ltd' 
        AND docstatus = 1
    """)

    total_rejected_value = total_rejected[0][0] if total_rejected and total_rejected[0][0] is not None else 0
    total_to_manufacture_value = total_to_manufacture[0][0] if total_to_manufacture and total_to_manufacture[0][0] is not None else 0

    if total_to_manufacture_value != 0:
        rejection_percentage = round(((total_rejected_value / total_to_manufacture_value) * 100),3)
    else:
        rejection_percentage = 0
    return {
        "value": rejection_percentage,
        "fieldtype": "Percent",
         "route_options": {
            "from_date": filters.get("from_date"),
            "to_date": filters.get("to_date"),
            "company": "RBD Castech Pvt Ltd" 
        },
        "route": ["query-report", "Rejection Analysis"]
    }

@frappe.whitelist()
def re_rejected_qty_weighted(filters = None):
    today = datetime.today().date()
    from_date = today - timedelta(days=7)

    filters = {
        "from_date": str(from_date),
        "to_date": str(today)
    }
    
    conditions = ""

    if filters.get("from_date") and filters.get("to_date"):
        conditions += f" AND Date(jc.creation) BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'"
        
    re_rejected_qty_weighted = frappe.db.sql(f"""
        SELECT
            SUM(jc.process_loss_qty * i.weight_per_unit) AS rejected_qty_weight
        FROM 
            `tabJob Card` as jc
        JOIN
		    `tabItem` i ON jc.production_item = i.item_code
        WHERE
            jc.status = 'Completed'{conditions} AND jc.company = 'RBD Engineers Pvt Ltd' AND jc.docstatus = 1
    """,as_dict=True)
    rejected_qty_weight = 0.000
    rejected_qty_weight = re_rejected_qty_weighted[0].rejected_qty_weight if re_rejected_qty_weighted and re_rejected_qty_weighted[0] is not None else 0.000
    rejected_qty_weight = round(rejected_qty_weight,3) 
    return {
        "value": rejected_qty_weight,
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
def rc_rejected_qty_weighted(filters = None):
    today = datetime.today().date()
    from_date = today - timedelta(days=7)

    filters = {
        "from_date": str(from_date),
        "to_date": str(today)
    }
    
    conditions = ""

    if filters.get("from_date") and filters.get("to_date"):
        conditions += f" AND Date(jc.creation) BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'"
        
    rc_rejected_qty_weighted = frappe.db.sql(f"""
        SELECT
            SUM(jc.process_loss_qty * i.weight_per_unit) AS rejected_qty_weight
        FROM 
            `tabJob Card` as jc
        JOIN
		    `tabItem` i ON jc.production_item = i.item_code
        WHERE
            jc.status = 'Completed'{conditions} AND jc.company = 'RBD Castech Pvt Ltd' AND jc.docstatus = 1
    """,as_dict=True)
    rejected_qty_weight = 0.000
    rejected_qty_weight = rc_rejected_qty_weighted[0].rejected_qty_weight if rc_rejected_qty_weighted and rc_rejected_qty_weighted[0] is not None else 0.000
    rejected_qty_weight = round(rejected_qty_weight,3) 
    return {
        "value": rejected_qty_weight,
        "fieldtype": "Float",
        "precision": "3",
        "route_options": {
            "from_date": filters.get("from_date"),
            "to_date": filters.get("to_date"),
            "company": 'RBD Castech Pvt Ltd'
        },
        "route": ["query-report", "Rejection Analysis"]
    }
    
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
        
    re_manufactured_qty_weighted = frappe.db.sql(f"""
        SELECT
            SUM(jc.total_completed_qty * i.weight_per_unit) AS rejected_qty_weight
        FROM 
            `tabJob Card` as jc
        JOIN
		    `tabItem` i ON jc.production_item = i.item_code
        WHERE
            jc.status = 'Completed'{conditions} AND jc.company = 'RBD Engineers Pvt Ltd' AND jc.docstatus = 1
    """,as_dict=True)
    
    manufactured_qty_weight = 0.000
    manufactured_qty_weight = re_manufactured_qty_weighted[0].rejected_qty_weight if re_manufactured_qty_weighted and re_manufactured_qty_weighted[0] is not None else 0.000
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
            jc.status = 'Completed'{conditions} AND jc.company = 'RBD Castech Pvt Ltd' AND jc.docstatus = 1
    """,as_dict=True)
    manufactured_qty_weight = 0.000
    manufactured_qty_weight = rc_manufactured_qty_weighted[0].rejected_qty_weight if rc_manufactured_qty_weighted and rc_manufactured_qty_weighted[0] is not None else 0.000
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