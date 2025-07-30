import frappe

def get_context(context):
    # Get employee ID from URL
    component_id = frappe.form_dict.get('id')
    doc = frappe.get_doc('Salary Structure', component_id)
    context.active_page = "salary-structure"
    docstatus = frappe.db.get_value('Salary Structure', component_id, 'docstatus')
    context.docstatus = docstatus
    context.component_id = doc.name
    return context
    