import frappe

def get_context(context):
    # Get employee ID from URL
    component_id = frappe.form_dict.get('id')
    context.component_id = component_id
    context.active_page = "component"
    return context
    