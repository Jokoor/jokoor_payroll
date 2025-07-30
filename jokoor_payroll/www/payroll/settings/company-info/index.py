import frappe

def get_context(context):
    # Get employee ID from URL
    doc = frappe.get_doc("Company", {"owner": frappe.session.user})
    context.company = doc.name
    context.active_page = "settings"
    return context
    