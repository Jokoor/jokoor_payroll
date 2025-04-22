import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/login?/dashboard/settings/salary-component"
        raise frappe.Redirect
    
    context.no_cache = 1
    context.title = "Salary Component"
    
    