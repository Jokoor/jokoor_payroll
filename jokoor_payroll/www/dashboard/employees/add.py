import frappe
from frappe import _
import erpnext


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?/dashboard/employees/add"
        raise frappe.Redirect 
    # Add necessary context variables
    context.departments = get_departments()
    context.positions = get_positions()

    # Add page metadata
    context.no_cache = 1
    context.show_sidebar = True  # Change from False to True
    context.no_breadcrumbs = True  # Hide Frappe's breadcrumbs

    # If there are other templates being included, you can disable them
    context.no_header = True
    context.no_footer = True

    return context


def get_departments():
    # Try to fetch from the database if Department doctype exists
    try:
        departments = frappe.get_all("Department", fields=["name"])
        return [d.name for d in departments]
    except:
        # Fallback to hardcoded list
        return [
            "HR",
            "Finance",
            "Engineering",
            "Marketing",
            "Sales",
            "Operations",
            "Customer Support",
        ]


def get_positions():
    # Try to fetch from the database if Designation doctype exists
    try:
        positions = frappe.get_all("Designation", fields=["name"])
        return [p.name for p in positions]
    except:
        # Fallback to hardcoded list
        return [
            "Manager",
            "Director",
            "Associate",
            "Specialist",
            "Coordinator",
            "Analyst",
            "Assistant",
            "Senior Developer",
            "Developer",
        ]


@frappe.whitelist()
def create_employee(
    first_name,
    last_name,
    email,
    position,
    department,
    date_of_birth=None,
    gender=None,
    address=None,
    phone=None,
    tax_id=None,
    date_of_joining=None,
    salary=None,
    employment_type="Full-time",
    status="Active",
):
    """
    Handle employee creation from form submission
    """
    try:
        # Create new employee document
        employee = frappe.new_doc("Employee")

        # Set employee fields from form data
        employee.first_name = first_name
        employee.last_name = last_name
        employee.personal_email = email
        employee.designation = position
        employee.department = department

        # Set optional fields if provided
        if date_of_birth:
            employee.date_of_birth = date_of_birth
        if gender:
            employee.gender = gender
        if address:
            employee.address_line1 = address
        if phone:
            employee.phone = phone
        if tax_id:
            employee.tax_id = tax_id
        if date_of_joining:
            employee.date_of_joining = date_of_joining
        if salary:
            employee.salary = float(salary)

        employee.employment_type = employment_type
        employee.status = status

        # Set company
        try:
            employee.company = frappe.defaults.get_user_default(
                "Company"
            ) or frappe.db.get_single_value("Global Defaults", "default_company")
        except:
            employee.company = "Company"  # Fallback to a default company name

        # Save the document
        employee.insert()
        frappe.db.commit()

        # Return success response
        return {
            "success": True,
            "message": "Employee created successfully",
            "employee_id": employee.name,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Employee Creation Error"))
        return {"success": False, "message": f"Error creating employee: {str(e)}"}
