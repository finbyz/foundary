import frappe
from frappe import _
import sys


def execute(filters=None):
    columns = get_column_data()
    data, columns = get_data(filters, columns)
    return columns, data


def get_column_data():
    return [
        {
            "label": _("Sales Order"),
            "fieldname": "sales_order",
            "fieldtype": "Link",
            "width": 150,
            "options": "Sales Order",
        },
        {
            "fieldname": "item_code",
            "label": _("Item Code"),
            "fieldtype": "Link",
            "width": 180,
            "options": "Item",
        },
        {
            "fieldname": "delivery_date",
            "label": _("Delivery Date"),
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "fieldname": "so_qty",
            "label": _("SO Qty"),
            "fieldtype": "Float",
            "width": 120,
        },
        {
            "fieldname": "delivered_qty",
            "label": _("Delivered Qty"),
            "fieldtype": "Float",
            "width": 120,
        },
        {
            "fieldname": "difference_qty",
            "label": _("Remaining Qty"),
            "fieldtype": "Float",
            "width": 120,
        },
        {
            "fieldname": "stock_qty",
            "label": _("Stock Qty"),
            "fieldtype": "Float",
            "width": 120,
        },
    ]


def get_data(filters, columns):
    condition = ""
    if filters.get("item_code"):
        condition += f"AND soi.item_code = '{filters.get('item_code')}'"

    # initializing dictionary for ignoring maximum depth limit
    item_all_child_warehouse_stoock = {}

    sales_order_data = frappe.db.sql(
        f"""
        SELECT so.name as sales_order, soi.item_code as item_code,so.delivery_date, soi.qty as so_qty, soi.delivered_qty as delivered_qty, soi.item_name as item_name
        FROM `tabSales Order` so
        INNER JOIN `tabSales Order Item` soi ON so.name = soi.parent
        WHERE so.company = "{filters.get('company')}" AND so.status NOT IN ("Completed", "Closed", "Cancelled") {condition}
    """,
        as_dict=True,
    )

    bin_data = get_bin_data_with_all_warehouse(filters)

    for sales_data in sales_order_data:
        sales_data["difference_qty"] = float(sales_data["so_qty"]) - float(
            sales_data["delivered_qty"]
        )

        # getting all the warehouse stock sum for the particular item_code
        sum_data = 0.00
        for b_data in bin_data:
            if b_data.item_code == sales_data.item_code:
                sum_data += float(b_data.actual_qty)

        sales_data["stock_qty"] = sum_data

        # getting all child bom data with respect toparent item code
        child_bom_data = get_child_data_with_respect_to_item_code(
            sales_data.item_code, item_all_child_warehouse_stoock, bin_data
        )

        for keys, values in child_bom_data.items():
            sales_data.update({keys: values})

    # getting all the warehouse list
    warehouse_list = get_all_the_warehouse_list(filters)

    for warehouse_name in warehouse_list:
        fieldname = f"{warehouse_name.name.replace('-', '').replace(' ', '_')}"
        new_dict = {
            "label": _(f"{warehouse_name.name}"),
            "fieldname": fieldname.lower(),
            "fieldtype": "Float",
            "width": 150,
        }
        columns.append(new_dict)


    return sales_order_data, columns


# getting all the actual qty,warehouse,item_code with respect to the company
def get_bin_data_with_all_warehouse(filters):
    bin_data = frappe.db.sql(
        f"""
       SELECT bin.item_code,bin.actual_qty,bin.warehouse
       FROM `tabBin` bin
       INNER JOIN `tabWarehouse` warehouse on warehouse.name=bin.warehouse
       WHERE warehouse.company="{filters.get('company')}" AND warehouse.is_group!=1 
    """,
        as_dict=True,
    )
    return bin_data


# getting all the warehouse list
def get_all_the_warehouse_list(filters):
    warehouse = frappe.db.sql(
        f"""
        SELECT warehouse.name as name
        FROM `tabWarehouse` warehouse
        WHERE warehouse.company = "{filters.get('company')}" AND warehouse.is_group!=1 
        ORDER BY warehouse.sequence_no
    """,
        as_dict=True,
    )
    return warehouse


# gettting nested child table details
def get_child_data_with_respect_to_item_code(item_code, item_all_child_warehouse_stoock, bin_data):
    if str(item_code) not in item_all_child_warehouse_stoock:
        item_all_child_warehouse_stoock[str(item_code)] = {}

    stack = [(item_code, [])]  
    memo = {} 

    while stack:
        current_item, parent_items = stack.pop()

        if current_item in memo:
            for key, value in memo[current_item].items():
                item_all_child_warehouse_stoock[str(item_code)][key] = item_all_child_warehouse_stoock[str(item_code)].get(key, 0) + value
            continue

        bom_data = frappe.db.sql(
            """
            SELECT bom_item.item_code as item_code, bom_item.item_name as item_name
            FROM `tabBOM` bom
            INNER JOIN `tabBOM Item` bom_item ON bom.name = bom_item.parent
            WHERE bom.item = %s AND bom.is_default = 1 AND bom.docstatus = 1
            """,
            (current_item,),
            as_dict=True,
        )

        if not bom_data:
            memo[current_item] = {}
            continue

        current_item_warehouse_data = {}
        for b_data in bin_data:
            if b_data.item_code == current_item:
                fieldname = f"{b_data.warehouse.replace('-', '').replace(' ', '_')}".lower()
                current_item_warehouse_data[fieldname] = b_data.actual_qty

        for item_data in bom_data:
            stack.append((item_data.item_code, parent_items + [current_item]))

        memo[current_item] = current_item_warehouse_data

        for key, value in current_item_warehouse_data.items():
            item_all_child_warehouse_stoock[str(item_code)][key] = item_all_child_warehouse_stoock[str(item_code)].get(key, 0) + value

    return item_all_child_warehouse_stoock[str(item_code)]