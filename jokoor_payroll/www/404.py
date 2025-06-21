import frappe
from frappe import _


def get_context(context):
    context.no_cache = 1

    # Get the current logged in employee
    employee_user = frappe.session.user

    if not employee_user or employee_user == "Guest":
        context.salary_slip = None
        return context

    # Try to get employee record for the current user
    employee = frappe.db.get_value("Employee", {"user_id": employee_user}, "name")

    if not employee:
        context.salary_slip = None
        return context

    # Get the most recent salary slip for this employee
    salary_slips = frappe.get_list(
        "Salary Slip",
        filters={
            "employee": employee,
            "docstatus": 1,  # Only get submitted salary slips
        },
        fields=["name"],
        order_by="posting_date desc",
        limit=1,
    )

    if not salary_slips:
        context.salary_slip = None
        return context

    # Get the full salary slip document
    context.salary_slip = frappe.get_doc("Salary Slip", salary_slips[0].name)

    return context
