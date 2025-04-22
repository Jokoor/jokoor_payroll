import frappe

@frappe.whitelist()
def get_employee_details(employee_id):
    return frappe.get_doc("Employee", employee_id)


def create_employee(employee_data):
    """
    Create a new employee record in the database.

    :param employee_data: Dictionary containing employee details
    :return: Success message or error
    """
    try:
        # Validate the employee data
        if not employee_data.get("first_name") or not employee_data.get("last_name"):
            return {
                "status": "error",
                "message": _("First name and last name are required."),
            }

        # Create a new employee document
        new_employee = frappe.get_doc(
            {
                "doctype": "Employee",
                "first_name": employee_data.get("first_name"),
                "last_name": employee_data.get("last_name"),
                "personal_email": employee_data.get("email"),
                "department": employee_data.get("department"),
                "designation": employee_data.get("designation"),
                "date_of_joining": employee_data.get("date_of_joining"),
                # Add other fields as necessary
            }
        )

        # Insert the new employee into the database
        new_employee.insert()
        frappe.db.commit()

        return {"status": "success", "message": _("Employee created successfully.")}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error creating employee"))
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def before_request():
    # if url have #login then redirect to login page
    if "#login" in frappe.request.url:
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
@frappe.whitelist(allow_guest=True)
def add_salary_component():
    form = frappe.request.form
    try:
        component_name = form.get("component_name")
        component_abbr = form.get("component_abbr")

        doc = frappe.get_doc({
            "doctype": "Salary Component",
            "salary_component": component_name,
            "salary_component_abbr": component_abbr,
            "type": "Earning"
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/dashboard/settings"
    except Exception as e:
        frappe.log_error(frappe.get_traceback(),("Error adding salary component"))
        return {"status": "error", "message": str(e)}
    

    
    return doc