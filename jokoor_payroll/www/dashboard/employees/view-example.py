import frappe
from frappe import _
from jokoor.utils import check_login

def get_context(context):
    # Ensure user is logged in
    check_login("/dashboard/employees/view-example")
    
    context.page_title = "Employee View"
    context.subtitle = "Employee details and information"
    context.has_search = False
    
    # Configure page buttons - enable both edit and actions
    context.is_editable = True  # Show the edit button
    context.target_form_id = "employeeForm"  # Target form ID for edit button
    context.page_entity = "Employee"  # Set entity name for edit button
    
    # Configure actions dropdown
    context.has_actions = True  # Show the actions dropdown
    context.action_items = [
        {
            "text": "Print Employee Data",
            "icon": "fa-print",
            "onclick": "printEmployeeData()"
        },
        {
            "text": "Export as PDF",
            "icon": "fa-file-pdf",
            "onclick": "exportEmployeeData()"
        },
        {
            "text": "Archive Employee",
            "icon": "fa-archive",
            "onclick": "archiveEmployee()"
        }
    ]
    
    # Define form parameters for the employee form
    context.form_id = "employeeForm"
    context.form_action = "/api/method/jokoor_payroll.api.update_employee"
    context.form_method = "POST"
    context.form_validate = True
    context.form_initial_state = "view"  # Start in view mode
    
    # Define breadcrumb for navigation
    context.breadcrumb_items = [
        {"label": "Dashboard", "url": "/dashboard"},
        {"label": "Employees", "url": "/dashboard/employees"},
        {"label": "Employee View", "url": "#"}
    ]
    
    # Sample employee data
    employee_data = {
        "employee_name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "gender": "Male",
        "designation": "Software Engineer",
        "department": "Engineering",
        "joining_date": "2023-01-15",
        "status": "Active"
    }
    
    # Define form sections
    context.form_sections = [
        {
            "title": "Personal Information",
            "icon": "fa-user",
            "description": "Basic employee information",
            "width": 12,
            "fields": [
                {
                    "type": "text",
                    "name": "employee_name",
                    "label": "Full Name",
                    "required": True,
                    "value": employee_data["employee_name"],
                    "width": 6
                },
                {
                    "type": "email",
                    "name": "email",
                    "label": "Email Address",
                    "required": True,
                    "value": employee_data["email"],
                    "width": 6
                },
                {
                    "type": "tel",
                    "name": "phone",
                    "label": "Phone Number",
                    "value": employee_data["phone"],
                    "width": 6
                },
                {
                    "type": "select",
                    "name": "gender",
                    "label": "Gender",
                    "value": employee_data["gender"],
                    "options": [
                        {"value": "Male", "label": "Male"},
                        {"value": "Female", "label": "Female"},
                        {"value": "Other", "label": "Other"}
                    ],
                    "width": 6
                }
            ]
        },
        {
            "title": "Employment Details",
            "icon": "fa-briefcase",
            "description": "Work-related information",
            "width": 12,
            "fields": [
                {
                    "type": "text",
                    "name": "designation",
                    "label": "Designation",
                    "value": employee_data["designation"],
                    "width": 6
                },
                {
                    "type": "text",
                    "name": "department",
                    "label": "Department",
                    "value": employee_data["department"],
                    "width": 6
                },
                {
                    "type": "date",
                    "name": "joining_date",
                    "label": "Joining Date",
                    "value": employee_data["joining_date"],
                    "width": 6
                },
                {
                    "type": "select",
                    "name": "status",
                    "label": "Status",
                    "value": employee_data["status"],
                    "options": [
                        {"value": "Active", "label": "Active"},
                        {"value": "Inactive", "label": "Inactive"},
                        {"value": "On Leave", "label": "On Leave"}
                    ],
                    "width": 6
                }
            ]
        }
    ]
