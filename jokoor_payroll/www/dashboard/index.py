import frappe
import random
from datetime import datetime, timedelta
import json
from frappe import _


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?/dashboard/"
        raise frappe.Redirect 

    context.total_employees = frappe.db.count("Employee")
    context.active_employees = frappe.db.count("Employee", {"status": "Active"})
    context.inactive_employees = frappe.db.count("Employee", {"status": "Inactive"})
    context.employee_list = frappe.db.get_list("Employee", fields=["*"], limit=10)
    context.gross_pay = gross_pay()
    context.pending_pay = pending_pay()
    context.total_tax_deduction = total_tax_deduction()
    context.payroll_activities = payroll_activities()
    return context


def gross_pay():
    gross_pay = frappe.db.sql(
        """
        SELECT 
            SUM(gross_pay) as total_gross_pay
        FROM 
            `tabSalary Slip`
        WHERE 
            docstatus = 1
    """
    )
    # format it to currency
    return frappe.utils.fmt_money(gross_pay[0][0])


def pending_pay():
    pending_pay = frappe.db.sql(
        """
        SELECT 
            SUM(gross_pay) as total_gross_pay
        FROM 
            `tabSalary Slip`
        WHERE 
            docstatus = 0
    """
    )
    return frappe.utils.fmt_money(pending_pay[0][0])


def total_tax_deduction():
    total_tax_deduction = frappe.db.sql(
        """
        SELECT 
            SUM(amount) as total_tax_deduction
        FROM 
            `tabSalary Detail`
        WHERE 
            salary_component in ("PAYEE", "SSHFC")
    """
    )
    return frappe.utils.fmt_money(total_tax_deduction[0][0])


def payroll_activities():
    activities = frappe.get_all(
        "Salary Slip",
        fields=["employee_name", "designation", "net_pay", "status"],
        limit=10,
    )
    data = []
    for activity in activities:
        initials = (
            activity.employee_name.split(" ")[0][0]
            + activity.employee_name.split(" ")[1][0]
        )
        data.append(
            {
                "employee_name": activity.employee_name,
                "designation": activity.designation,
                "net_pay": activity.net_pay,
                "status": activity.status,
                "image": frappe.db.get_value(
                    "Employee", activity.employee_name, "image"
                ),
                "initials": initials,
            }
        )
    return data

