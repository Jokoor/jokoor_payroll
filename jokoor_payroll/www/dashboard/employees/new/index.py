import frappe
from frappe import _
from frappe.utils import cint, flt, getdate, now_datetime
import re


def get_context(context):
    """
    Prepare context data for the employee add page
    """
    if frappe.session.user == "Guest":
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = (
            "/login?redirect-to=/dashboard/employees/new"
        )
        return

    # Check if the user has permission to add employees
    if not frappe.has_permission("Employee", "create"):
        frappe.throw(_("You don't have permission to add employees"))

    # Get all departments
    context.departments = frappe.get_all("Department", fields=["name"])

    # Get all designations
    context.designations = frappe.get_all("Designation", fields=["name"])

    # Get all employees for reporting manager dropdown
    context.employees = frappe.get_all("Employee", fields=["name", "employee_name"])

    # Pass any form messages
    context.message = frappe.form_dict.get("message")
    context.success = frappe.form_dict.get("success")

    return context


@frappe.whitelist()
def save_employee():
    """
    Save employee data submitted from the form
    """
    try:
        # Check permission
        if not frappe.has_permission("Employee", "create"):
            frappe.throw(_("You don't have permission to add employees"))

        # Get form data
        first_name = frappe.form_dict.get("first_name")
        last_name = frappe.form_dict.get("last_name")
        gender = frappe.form_dict.get("gender")
        date_of_birth = frappe.form_dict.get("date_of_birth")
        email = frappe.form_dict.get("email")
        phone = frappe.form_dict.get("phone")

        # Validate required fields
        validate_required_fields()

        # Create employee name
        employee_name = f"{first_name} {last_name}"

        # Check for existing employee with same email
        if frappe.db.exists("Employee", {"personal_email": email}):
            frappe.msgprint(_("An employee with this email already exists"))
            frappe.local.response["type"] = "redirect"
            frappe.local.response["location"] = (
                "/dashboard/employees/new?message=An+employee+with+this+email+already+exists&success=0"
            )
            return

        # Generate employee ID if not provided
        employee_id = frappe.form_dict.get("employee_id")
        if not employee_id:
            employee_id = generate_employee_id()

        # Create new employee
        employee = frappe.new_doc("Employee")

        # Set basic information
        employee.first_name = first_name
        employee.last_name = last_name
        employee.employee_name = employee_name
        employee.gender = gender
        employee.date_of_birth = date_of_birth
        employee.marital_status = frappe.form_dict.get("marital_status")

        # Set identification information
        employee.tin_no = frappe.form_dict.get("tin_no")
        employee.bban = frappe.form_dict.get("bban")
        employee.social_security_number = frappe.form_dict.get("social_security_number")

        # Set contact information
        employee.personal_email = email
        employee.company_email = email  # Can be same as personal email initially
        employee.cell_number = phone
        employee.permanent_address = frappe.form_dict.get("address")
        employee.permanent_accommodation_type = ""  # Optional field

        # Set employment details
        employee.department = frappe.form_dict.get("department")
        employee.designation = frappe.form_dict.get("designation")
        employee.employment_type = frappe.form_dict.get("employment_type")
        employee.date_of_joining = frappe.form_dict.get("date_of_joining")
        employee.status = frappe.form_dict.get("status")
        employee.reports_to = frappe.form_dict.get("reports_to") or None

        # Set bank information
        employee.salary_mode = frappe.form_dict.get("salary_mode")

        if employee.salary_mode == "Bank":
            employee.bank_name = frappe.form_dict.get("bank_name")
            employee.bank_ac_no = frappe.form_dict.get("bank_ac_no")
            employee.account_name = frappe.form_dict.get("account_name")

        # Save the employee
        employee.insert(ignore_permissions=True)

        # Create a salary structure assignment if base_salary is provided
        base_salary = flt(frappe.form_dict.get("base_salary") or 0)
        if base_salary > 0:
            create_salary_structure_assignment(employee.name, base_salary)

        # Determine where to redirect based on save action
        save_action = frappe.form_dict.get("save_action")
        if save_action == "save_and_new":
            frappe.local.response["type"] = "redirect"
            frappe.local.response["location"] = (
                "/dashboard/employees/new?message=Employee+added+successfully&success=1"
            )
        else:
            frappe.local.response["type"] = "redirect"
            frappe.local.response["location"] = (
                f"/dashboard/employees/view?id={employee.name}&message=Employee+added+successfully&success=1"
            )

    except Exception as e:
        frappe.log_error(f"Error saving employee: {str(e)}")
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = (
            f"/dashboard/employees/new?message=Error+saving+employee:+{str(e)}&success=0"
        )


def validate_required_fields():
    """
    Validate that all required fields are provided
    """
    required_fields = [
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
        "email",
        "phone",
        "department",
        "designation",
        "employment_type",
        "date_of_joining",
        "status",
    ]

    for field in required_fields:
        if not frappe.form_dict.get(field):
            frappe.throw(_(f"Field {field.replace('_', ' ').title()} is required"))

    # Validate email format
    email = frappe.form_dict.get("email")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        frappe.throw(_("Please enter a valid email address"))

    # Validate date of birth (must be at least 18 years ago)
    dob = getdate(frappe.form_dict.get("date_of_birth"))
    today = getdate()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if age < 18:
        frappe.throw(_("Employee must be at least 18 years old"))


def generate_employee_id():
    """
    Generate a unique employee ID
    """
    # Get company prefix (you can customize this based on your needs)
    prefix = "EMP"

    # Get current year
    year = now_datetime().year

    # Count existing employees this year and add 1
    count = frappe.db.count("Employee") + 1

    # Format: EMP-YYYY-00001
    employee_id = f"{prefix}-{year}-{count:05d}"

    # Ensure it's unique
    while frappe.db.exists("Employee", {"name": employee_id}):
        count += 1
        employee_id = f"{prefix}-{year}-{count:05d}"

    return employee_id


def create_salary_structure_assignment(employee, base_salary):
    """
    Create a salary structure assignment for the employee
    """
    # First, check if a default salary structure exists
    default_structure = frappe.db.get_single_value(
        "HR Settings", "default_salary_structure"
    )

    if not default_structure:
        # Create basic salary structure if it doesn't exist
        structure_name = "Basic Salary Structure"
        if not frappe.db.exists("Salary Structure", structure_name):
            create_basic_salary_structure(structure_name)
        default_structure = structure_name

    # Create salary structure assignment
    assignment = frappe.new_doc("Salary Structure Assignment")
    assignment.employee = employee
    assignment.salary_structure = default_structure
    assignment.base = base_salary
    assignment.from_date = frappe.form_dict.get("date_of_joining")

    # Save the assignment
    assignment.insert(ignore_permissions=True)

    return assignment


def create_basic_salary_structure(name):
    """
    Create a basic salary structure if it doesn't exist
    """
    salary_structure = frappe.new_doc("Salary Structure")
    salary_structure.name = name
    salary_structure.salary_slip_based_on_timesheet = 0

    # Add basic salary component
    basic_component = frappe.db.get_value("Salary Component", {"name": "Basic"})
    if not basic_component:
        basic_component = create_basic_salary_component()

    salary_structure.append(
        "earnings",
        {
            "salary_component": "Basic",
            "formula": "base",
            "amount_based_on_formula": 1,
            "abbr": "B",
        },
    )

    # Save the structure
    salary_structure.insert(ignore_permissions=True)

    return salary_structure.name


def create_basic_salary_component():
    """
    Create a basic salary component if it doesn't exist
    """
    component = frappe.new_doc("Salary Component")
    component.name = "Basic"
    component.salary_component = "Basic"
    component.type = "Earning"
    component.is_tax_applicable = 1
    component.salary_component_abbr = "B"

    component.insert(ignore_permissions=True)

    return component.name
