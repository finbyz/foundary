# Copyright (c) 2023, FinByz Tech Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import _

# intitializing list for getting its all item bom
bom_dict=[]
bom_hashed_value={}

def execute(filters=None):
    columns = get_column_data()
    data, columns = get_data(filters, columns)
    return columns, data

def get_column_data():
    return [
        {
            'label': _('Sales Order'),
            'fieldname': 'sales_order',
            'fieldtype': 'Link',
            'width': 150,
            'options': 'Sales Order'
        },
        {
            "fieldname": "item_code",
            "label": _("Item Code"),
            "fieldtype": "Link",
            "width": 180,
            'options': 'Item'
        },
        {
            "fieldname": "so_qty",
            "label": _("SO Qty"),
            "fieldtype": "Float",
            "width": 120
        },
        {
            "fieldname": "delivered_qty",
            "label": _("Delivered Qty"),
            "fieldtype": "Float",
            "width": 120
        },
        {
            "fieldname": "difference_qty",
            "label": _("Remaining Qty"),
            "fieldtype": "Float",
            "width": 120
        },
        {
            "fieldname": "stock_qty",
            "label": _("Stock Qty"),
            "fieldtype": "Data",
            "width": 120
        }
    ]

def get_data(filters, columns):
    global bom_dict
    bom_dict = []
    global bom_hashed_value
    bom_hashed_value={}

    sales_order_data = frappe.db.sql(f"""
        SELECT so.name as sales_order, soi.item_code as item_code, soi.qty as so_qty, soi.delivered_qty as delivered_qty, soi.item_name as item_name
        FROM `tabSales Order` so
        INNER JOIN `tabSales Order Item` soi ON so.name = soi.parent
        WHERE so.company = "{filters.get('company')}" AND so.status NOT IN ("Completed", "Closed", "Cancelled")
    """, as_dict=True)

    new_columns = []


    for sales_data in sales_order_data:
        sum_data = get_actual_quantity_of_item_from_all_warehouse(sales_data.item_code)
        sales_data['stock_qty'] = sum_data
        sales_data['difference_qty'] = float(sales_data['so_qty']) - float(sales_data['delivered_qty'])

        warehouse_data = get_warehouse_respect_to_the_item(sales_data.item_code)
        for w_data in warehouse_data:
            fieldname = f"{w_data.warehouse.replace('-', '').replace(' ', '_')}"
            sales_data[fieldname] = w_data.actual_qty

            new_dict = {
                'label': _(f'{w_data.warehouse}'),
                'fieldname': fieldname,
                'fieldtype': 'Float',
                'width': 150
            }

            # making dyanamic column
            if new_dict not in new_columns:
                new_columns.append(new_dict)
        
        #getting item and its total child_sum with respect to the warehouse
        dict_data=get_child_bom_data_with_parent_item_code(sales_data.item_name)

        if dict_data:
            for key,value in dict_data.items():
                fieldname = f"{key.replace('-', '').replace(' ', '_')}"
                sales_data[fieldname]+=value


    columns.extend(new_columns)

    return sales_order_data, columns

def get_actual_quantity_of_item_from_all_warehouse(item_code):
    actual_quantity_sum = frappe.db.sql("""
        SELECT SUM(actual_qty) as sum
        FROM `tabBin` 
        WHERE item_code = %s 
    """, item_code, as_dict=True)

    return actual_quantity_sum[0].sum

def get_warehouse_respect_to_the_item(item_code):
    warehouse_data = frappe.db.sql("""
        SELECT warehouse, actual_qty
        FROM `tabBin` 
        WHERE item_code = %s
    """, item_code, as_dict=True)

    return warehouse_data


#getting child data with parent_bom
def get_child_bom_data_with_parent_item_code(item_name):

    global bom_dict
    if item_name in bom_dict:
        if item_name not in bom_hashed_value.keys():
            return {}
        return bom_hashed_value[item_name]
    
    #adding the value into list
    bom_dict.append(item_name)
    
    
    bom_data= frappe.db.sql("""
        SELECT bom_item.item_code as item_code,bom_item.item_name as item_name
        FROM `tabBOM` bom
        INNER JOIN `tabBOM Item` bom_item on bom.name=bom_item.parent
        WHERE bom_item.item_name = %s AND bom.is_default=1
    """, item_name, as_dict=True)


    if  len(bom_data)==0:
        return {}
    
    current_dict={}

    # gettting nested child item_bom with respect to parent
    for item_data in bom_data:
        dict_data=get_child_bom_data_with_parent_item_code(item_data.item_name)

        #getting warehouse qty
        warehouse_qty=get_warehouse_respect_to_the_item(item_data.item_name)
        
        for w_q in warehouse_qty:
            key=w_q['warehouse']
            actual_qty=w_q['actual_qty']
            if key not in dict_data.keys():
                fieldname = f"{key.replace('-', '').replace(' ', '_')}"
                dict_data[fieldname]=float(actual_qty)
            else:
                fieldname = f"{key.replace('-', '').replace(' ', '_')}"
                dict_data[fieldname]+=float(actual_qty)

        for key,values in dict_data.items():
            if key not in current_dict.keys():
                current_dict[key]=values
            else:
                current_dict[key]+=values

    #adding value in hashed dictionaries
    bom_hashed_value.update({item_name: current_dict})

    return current_dict