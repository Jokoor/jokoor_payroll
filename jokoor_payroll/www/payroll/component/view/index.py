import frappe

def get_context(context):
    # Get employee ID from URL
    component_id = frappe.form_dict.get('id')
    doc = frappe.get_doc('Salary Component', component_id)
    context.active_page = "component"
    docstatus = frappe.db.get_value('Salary Component', component_id, 'docstatus')
    context.docstatus = docstatus
    context.component_id = doc.name
    return context
    