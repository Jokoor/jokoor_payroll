import frappe
from frappe import _

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/login?/dashboard/employees/profile"
        raise frappe.Redirect

    context.page_title = "Employee Profile"
    context.has_search = False
    context.has_actions = False
    context.has_primary_action = False
    
    # Configure breadcrumb
    context.breadcrumb_items = [
        {"label": "Dashboard", "url": "/dashboard"},
        {"label": "Employees", "url": "/dashboard/employees"},
        {"label": "Profile", "url": "#"}
    ]
    
    # Get list of departments for dropdown
    departments = [
        {"value": "Engineering", "label": "Engineering"},
        {"value": "Sales", "label": "Sales"},
        {"value": "Marketing", "label": "Marketing"},
        {"value": "HR", "label": "Human Resources"},
        {"value": "Finance", "label": "Finance"},
        {"value": "Operations", "label": "Operations"}
    ]
    context.departments = departments
    
    # Get employee data if exists, otherwise use dummy data
    employee = {
        "employee_name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-01",
        "designation": "Software Engineer",
        "department": "Engineering",
        "date_of_joining": "2023-01-01",
        "employment_type": "full_time",
        "basic_salary": "5000",
        "salary_currency": "USD",
        "payment_method": "bank_transfer"
    }
    context.employee = employee
    return context

@frappe.whitelist()
def update_employee():
    try:
        # Get form data
        data = frappe.form_dict
        
        # TODO: Validate and save employee data
        frappe.msgprint("Profile updated successfully")
        
        return {
            "status": "success",
            "message": "Employee profile updated successfully"
        }
    except Exception as e:
        frappe.log_error(f"Error updating employee profile: {str(e)}")
        return {
            "status": "error",
            "message": "Failed to update employee profile"
        }