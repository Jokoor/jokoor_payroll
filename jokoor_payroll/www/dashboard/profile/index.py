
import frappe
from frappe.utils import get_abbr


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?/dashboard/profile"
        raise frappe.Redirect   
    context.user = frappe.session.user
    user_info = frappe.get_doc("User", context.user)
    context.user_info = user_info
    user_initials = get_abbr(user_info.full_name)
    context.user_initials = user_initials
    return context

def update_profile(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect=/dashboard/profile"
        raise frappe.Redirect   
    user_info = frappe.get_doc("User", context.user)
    user_info.update(context.user_info)
    user_info.save()
    