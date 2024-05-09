import frappe
from frappe.utils import flt

@frappe.whitelist()
def get_party_details(party,):
    data=frappe.get_all("Bank Account", fields=["name","ifs_code","bank_account_no"], filters={"party": party})
    return {"data":data,"len":len(data)}