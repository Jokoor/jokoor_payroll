import frappe

def get_context(context):
    # Get employee ID from URL
    employee_id = frappe.form_dict.get('id')
    context.employee_id = employee_id
    context.active_page = "employees"
    context.title = "Employee"
    context.url = f"employee/{employee_id}"
    context.is_editable = True
    
    return context
    