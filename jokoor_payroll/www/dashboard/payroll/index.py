import frappe
from frappe.utils import get_abbr

def get_context(context):
    
    context.user = frappe.session.user
    context.user_info = frappe.get_doc("User", context.user)
    context.user_initials = get_abbr(context.user_info.full_name)
    return context

