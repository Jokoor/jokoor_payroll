import frappe
import random
from datetime import datetime, timedelta
import json
from frappe import _


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?/dashboard/employees"
        raise frappe.Redirect 
    context.employees = get_employees()
    context.departments = get_departments()
    context.positions = get_positions()
    context.total_employees = frappe.db.count("Employee")
    context.active_employees = frappe.db.count("Employee", {"status": "Active"})
    context.inactive_employees = frappe.db.count("Employee", {"status": "Inactive"})
    context.employee_list = frappe.db.get_list("Employee", fields=["*"], limit=10)

    return context


def get_employees():
    # Existing employee fetching code
    # ... existing code ...
    employees = frappe.db.get_list("Employee", fields=["*"], limit=10)
    return employees


def get_departments():
    # Return list of departments for the dropdown
    departments = [
        "HR",
        "Finance",
        "Engineering",
        "Marketing",
        "Sales",
        "Operations",
        "Customer Support",
    ]
    return departments


def get_positions():
    # Return list of positions for the dropdown
    positions = [
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
    return positions

