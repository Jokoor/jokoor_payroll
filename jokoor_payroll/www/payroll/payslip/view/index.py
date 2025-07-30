import frappe

def get_context(context):
    # Get employee ID from URL
    payslip_id = frappe.form_dict.get('id')
    doc = frappe.get_doc('Salary Slip', payslip_id)
    context.active_page = "payslip"
    docstatus = frappe.db.get_value('Salary Slip', payslip_id, 'docstatus')
    context.docstatus = docstatus
    context.payslip_id = doc.name
    return context
    