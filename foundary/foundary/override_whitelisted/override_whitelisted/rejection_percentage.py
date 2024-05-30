import frappe
import json

@frappe.whitelist()
def get_rejection_percentage_for_number_card(filters):
    filters = json.loads(filters)  # Parse the JSON string into a dictionary
    conditions = ""

    if filters.get("from_date") and filters.get("to_date"):
        conditions += f" AND Date(jc.posting_date) BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'"
        
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
            SUM(jc.for_quantity) AS total_to_manufacture
        FROM 
            `tabJob Card` as jc
        WHERE
            jc.status = 'Completed'{conditions} AND jc.company = 'RBD Engineers Pvt Ltd'
    """)
    
    total_rejected_value = total_rejected[0][0] if total_rejected and total_rejected[0][0] is not None else 0
    total_to_manufacture_value = total_to_manufacture[0][0] if total_to_manufacture and total_to_manufacture[0][0] is not None else 0

    if total_to_manufacture_value != 0:
        rejection_percentage = (total_rejected_value / total_to_manufacture_value) * 100
    else:
        rejection_percentage = 0

    return {
        "value": rejection_percentage,
        "fieldtype": "Percent",
        "route_options": {"from_date": filters.get("from_date")},
        "route": ["query-report", "Rejection Analysis"]
    }


import frappe
import json

@frappe.whitelist()
def get_rejection_percentage_for_number_card_castech(filters):
    filters = json.loads(filters)  # Parse the JSON string into a dictionary
    conditions = ""

    if filters.get("from_date") and filters.get("to_date"):
        conditions += f" AND Date(jc.posting_date) BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'"
        
    total_rejected = frappe.db.sql(f"""
        SELECT
            SUM(jc.process_loss_qty) AS total_rejected
        FROM 
            `tabJob Card` as jc
        WHERE
            jc.status = 'Completed'{conditions} AND jc.company = 'RBD Castech Pvt Ltd'
    """)

    total_to_manufacture = frappe.db.sql(f"""
        SELECT
            SUM(jc.for_quantity) AS total_to_manufacture
        FROM 
            `tabJob Card` as jc
        WHERE
            jc.status = 'Completed'{conditions} AND jc.company = 'RBD Castech Pvt Ltd'
    """)
    
    total_rejected_value = total_rejected[0][0] if total_rejected and total_rejected[0][0] is not None else 0
    total_to_manufacture_value = total_to_manufacture[0][0] if total_to_manufacture and total_to_manufacture[0][0] is not None else 0

    if total_to_manufacture_value != 0:
        rejection_percentage = (total_rejected_value / total_to_manufacture_value) * 100
    else:
        rejection_percentage = 0

    return {
        "value": rejection_percentage,
        "fieldtype": "Percent",
        "route_options": {"from_date": filters.get("from_date")},
        "route": ["query-report", "Rejection Analysis"]
    }
