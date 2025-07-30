import frappe
from jokoor.utils import handle_login

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.response.type = "redirect"
        frappe.local.response.location = "/login?redirect-to=/payroll/employees"
    
    context.active_page = 'employees'
    context.active_section = 'employees'
    context.title = "Employee List"
    context.subtitle = "Manage your employee records"
    context.add_new_url = "/payroll/employees/new"

    if frappe.request.args.get("per_page"):
        per_page = int(frappe.request.args.get("per_page"))
    else:
        per_page = 20
    
    # Define table columns
    context.columns = [
        {"key": "name", "label": "Employee ID"},
        {"key": "employee_name", "label": "Employee Name"},
        {"key": "designation", "label": "Employee Designation"},
        {"key": "gender", "label": "Gender"},
        {"key": "status_html", "label": "Status"}
    ]
    
    # Get employee data
    employee_list = frappe.get_list(
        "Employee", 
        fields=["name", "employee_name", "designation", "gender", "status"], 
        limit=per_page
    )
    
    # Process employee data
    for employee in employee_list:
        employee.url = f"/payroll/employees/view?id={employee.name}"
        if employee.status == "Active":
            employee.status_html = '<span class="badge badge-success">Active</span>'
        else:
            employee.status_html = '<span class="badge badge-danger">Inactive</span>'
    
    context.data = employee_list
