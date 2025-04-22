import frappe
import random
from faker import Faker
from frappe.utils import now_datetime, pretty_date, getdate, now, get_month


def get_context(context):
    """Generates context for a specific company profile based on query parameter"""
    # Get the company name from query parameters
    employee_id = frappe.form_dict.id
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?/dashboard/employees/view?id=" + employee_id
        raise frappe.Redirect

    # Debug output to frappe logs
    frappe.logger().info(f"Looking up employee with id: {employee_id}")

    if not employee_id:
        frappe.throw("No employee id provided")

    # Generate the company data - in a real-world app, you would query your database here
    context.employee = get_employee_by_id(employee_id)
    context.earnings, context.deductions = get_employee_salary_structure(employee_id)
    context.recent_payslips = get_employee_recent_payslips(employee_id)
    context.salary = get_employee_compensation(employee_id)

    # Get last raise information
    context.last_raise = get_last_raise(employee_id)

    # Get work anniversary information
    context.work_anniversary = get_work_anniversary(employee_id)

    # Get employment timeline
    context.employment_timeline = get_employment_timeline(employee_id)

    return context


def get_employee_by_id(employee_id):
    employee = frappe.get_doc("Employee", employee_id, as_dict=True)

    return employee


def get_employee_salary_structure(employee_id):
    salary_structure = frappe.db.get_value(
        "Salary Structure Assignment", {"employee": employee_id}, "salary_structure"
    )
    if not salary_structure:
        return [], []
    doc = frappe.get_doc("Salary Structure", salary_structure)
    earnings = []
    deductions = []
    for item in doc.earnings:
        earnings.append(
            {
                "name": item.salary_component,
                "amount": frappe.utils.fmt_money(item.amount),
            }
        )
    for item in doc.deductions:
        deductions.append(
            {
                "name": item.salary_component,
                "amount": frappe.utils.fmt_money(item.amount),
            }
        )
    return earnings, deductions


def get_employee_recent_payslips(employee_id):
    payslips = frappe.db.get_all(
        "Salary Slip",
        filters={"employee": employee_id},
        order_by="posting_date desc",
        limit=10,
    )
    payslips_list = []
    for payslip in payslips:
        payslip_doc = frappe.get_doc("Salary Slip", payslip.name)

        status = ""
        if payslip_doc.status == "Submitted":
            status = "Paid"
        elif payslip_doc.status == "Draft":
            status = "Pending"

        payslips_list.append(
            {
                "name": payslip.name,
                "posting_date": payslip_doc.posting_date,
                "amount": f"GMD {frappe.utils.fmt_money(payslip_doc.net_pay)}",
                "pay_period": f"{payslip_doc.start_date} - {payslip_doc.end_date}",
                "payment_date": getdate(payslip_doc.posting_date),
                "gross_pay": f"GMD {frappe.utils.fmt_money(payslip_doc.gross_pay)}",
                "deductions": f"GMD {frappe.utils.fmt_money(payslip_doc.total_deduction)}",
                "net_pay": f"GMD {frappe.utils.fmt_money(payslip_doc.net_pay)}",
                "status": status,
            }
        )
    return payslips_list


def get_employee_compensation(employee_id):
    salary_structure = frappe.db.get_value(
        "Salary Structure Assignment", {"employee": employee_id}, "salary_structure"
    )
    if not salary_structure:
        return f"GMD {frappe.utils.fmt_money(0)}"
    doc = frappe.get_doc("Salary Structure", salary_structure)
    amount = 0
    for item in doc.earnings:
        amount += item.amount
    return f"GMD {frappe.utils.fmt_money(amount)}"


def get_last_raise(employee_id):
    """
    Determine the last salary raise for an employee by comparing the most recent
    salary structure assignment with the previous one.

    Args:
        employee_id (str): The ID of the employee

    Returns:
        dict: Information about the last raise including date, previous amount,
              current amount, percentage change, and a formatted description
    """
    # Fetch all salary structure assignments for this employee, ordered by date
    salary_assignments = frappe.get_all(
        "Salary Structure Assignment",
        filters={"employee": employee_id},
        fields=["name", "salary_structure", "base", "from_date"],
        order_by="from_date desc",
    )

    # If fewer than 2 assignments, there's no way to determine a raise
    if len(salary_assignments) < 2:
        return {
            "has_raise": False,
            "description": "No previous salary data available",
            "raise_date": None,
            "percentage": 0,
            "previous_amount": 0,
            "current_amount": (
                salary_assignments[0]["base"] if salary_assignments else 0
            ),
        }

    # Get the current (most recent) and previous assignments
    current = salary_assignments[0]
    previous = salary_assignments[1]

    # Calculate the difference and percentage
    current_amount = current["base"]
    previous_amount = previous["base"]

    difference = current_amount - previous_amount

    # Avoid division by zero
    if previous_amount > 0:
        percentage = (difference / previous_amount) * 100
    else:
        percentage = 0

    # Format the date
    raise_date = current["from_date"]
    formatted_date = frappe.utils.formatdate(raise_date)

    # Create description
    if difference > 0:
        description = f"{formatted_date} (+{percentage:.1f}%)"
    elif difference < 0:
        description = f"{formatted_date} ({percentage:.1f}%)"
    else:
        description = f"{formatted_date} (No change)"

    return {
        "has_raise": difference != 0,
        "description": description,
        "raise_date": raise_date,
        "formatted_date": formatted_date,
        "percentage": percentage,
        "previous_amount": previous_amount,
        "current_amount": current_amount,
        "difference": difference,
    }


def get_work_anniversary(employee_id):
    """
    Calculate work anniversary details for an employee.

    Args:
        employee_id (str): The ID of the employee

    Returns:
        dict: Information about the employee's work anniversary including
              years completed, next anniversary date, days until next anniversary,
              and a formatted description
    """
    employee = frappe.get_doc("Employee", employee_id)

    if not employee.date_of_joining:
        return {
            "has_anniversary": False,
            "description": "No joining date available",
            "years_completed": 0,
            "next_anniversary": None,
            "days_until_next": 0,
        }

    # Current date and joining date
    today = getdate()
    joining_date = getdate(employee.date_of_joining)

    # Calculate completed years
    years_completed = today.year - joining_date.year

    # Adjust if haven't reached anniversary day this year
    if today.month < joining_date.month or (
        today.month == joining_date.month and today.day < joining_date.day
    ):
        years_completed -= 1

    # Calculate next anniversary date
    next_anniversary_year = today.year

    # If this year's anniversary has passed, next is next year
    if today.month > joining_date.month or (
        today.month == joining_date.month and today.day >= joining_date.day
    ):
        next_anniversary_year += 1

    next_anniversary = getdate(
        f"{next_anniversary_year}-{joining_date.month:02d}-{joining_date.day:02d}"
    )

    # Calculate days until next anniversary
    from datetime import datetime

    today_datetime = datetime.combine(today, datetime.min.time())
    next_ann_datetime = datetime.combine(next_anniversary, datetime.min.time())
    days_until_next = (next_ann_datetime - today_datetime).days

    # Format joining date
    formatted_joining = frappe.utils.formatdate(joining_date)

    # Create description
    if years_completed == 0:
        if days_until_next == 0:
            description = f"Today is their first day!"
        else:
            description = (
                f"Joined on {formatted_joining} ({days_until_next} days until 1 year)"
            )
    else:
        suffix = "s" if years_completed > 1 else ""
        if days_until_next == 0:
            description = f"Today is their {years_completed + 1}-year anniversary!"
        else:
            description = f"{years_completed} year{suffix} ({days_until_next} days until next anniversary)"

    return {
        "has_anniversary": True,
        "description": description,
        "years_completed": years_completed,
        "joining_date": joining_date,
        "formatted_joining": formatted_joining,
        "next_anniversary": next_anniversary,
        "days_until_next": days_until_next,
    }


def get_employment_timeline(employee_id):
    """
    Generate a comprehensive timeline of an employee's employment history
    focusing on payroll-related events.

    Args:
        employee_id (str): The ID of the employee

    Returns:
        list: Chronologically sorted timeline events with date, title, description, and type
    """
    timeline_events = []
    employee = frappe.get_doc("Employee", employee_id)

    # Add joining date event
    if employee.date_of_joining:
        timeline_events.append(
            {
                "date": employee.date_of_joining,
                "formatted_date": frappe.utils.formatdate(employee.date_of_joining),
                "title": "Employee Hired",
                "description": f"Joined as {employee.designation}",
                "type": "joining",
                "icon": "fa-user-plus",
            }
        )

    # Get all salary structure assignments
    salary_assignments = frappe.get_all(
        "Salary Structure Assignment",
        filters={"employee": employee_id},
        fields=["name", "salary_structure", "base", "from_date"],
        order_by="from_date asc",
    )

    # Add first salary assignment if exists
    if salary_assignments and len(salary_assignments) > 0:
        first_assignment = salary_assignments[0]
        salary_structure_name = frappe.db.get_value(
            "Salary Structure", first_assignment["salary_structure"], "name"
        )

        timeline_events.append(
            {
                "date": first_assignment["from_date"],
                "formatted_date": frappe.utils.formatdate(
                    first_assignment["from_date"]
                ),
                "title": "Initial Compensation",
                "description": f"Assigned to salary structure: {salary_structure_name} - Base: {frappe.utils.fmt_money(first_assignment['base'])}",
                "type": "salary",
                "icon": "fa-money-bill",
            }
        )

    # Add salary changes/raises (skip the first one as we already added it)
    for i in range(1, len(salary_assignments)):
        current = salary_assignments[i]
        previous = salary_assignments[i - 1]

        difference = current["base"] - previous["base"]
        percentage = (
            (difference / previous["base"] * 100) if previous["base"] > 0 else 0
        )

        if difference > 0:
            event_title = "Salary Increase"
            change_text = f"+{frappe.utils.fmt_money(difference)} (+{percentage:.1f}%)"
        elif difference < 0:
            event_title = "Salary Adjustment"
            change_text = f"{frappe.utils.fmt_money(difference)} ({percentage:.1f}%)"
        else:
            event_title = "Salary Structure Change"
            change_text = "No change in base amount"

        timeline_events.append(
            {
                "date": current["from_date"],
                "formatted_date": frappe.utils.formatdate(current["from_date"]),
                "title": event_title,
                "description": f"Base changed from {frappe.utils.fmt_money(previous['base'])} to {frappe.utils.fmt_money(current['base'])} - {change_text}",
                "type": "salary_change",
                "icon": "fa-chart-line",
            }
        )

    # Try to safely get employee job changes/promotions
    try:
        # First, check if the doctype exists
        if frappe.db.exists("DocType", "Employee Promotion"):
            # Try to get field names
            fields = frappe.get_meta("Employee Promotion").get_fieldnames_with_value()

            # Build a list of fields we want, if they exist
            promotion_fields = ["promotion_date"]

            # Add designation fields if they exist (account for different naming conventions)
            if "from_designation" in fields and "to_designation" in fields:
                promotion_fields.extend(["from_designation", "to_designation"])
            elif "old_designation" in fields and "new_designation" in fields:
                promotion_fields.extend(["old_designation", "new_designation"])
            elif "current_designation" in fields and "new_designation" in fields:
                promotion_fields.extend(["current_designation", "new_designation"])

            # Only attempt to query if we have the necessary fields
            if len(promotion_fields) >= 3:  # At least date and two designation fields
                employee_promotions = frappe.get_all(
                    "Employee Promotion",
                    filters={"employee": employee_id},
                    fields=promotion_fields,
                    order_by="promotion_date asc",
                )

                # Add promotions to timeline
                for promotion in employee_promotions:
                    # Determine which fields to use
                    old_desig_field = [
                        f
                        for f in promotion_fields
                        if f != "promotion_date"
                        and f.startswith(("from_", "old_", "current_"))
                    ][0]
                    new_desig_field = [
                        f
                        for f in promotion_fields
                        if f != "promotion_date" and f.startswith(("to_", "new_"))
                    ][0]

                    timeline_events.append(
                        {
                            "date": promotion["promotion_date"],
                            "formatted_date": frappe.utils.formatdate(
                                promotion["promotion_date"]
                            ),
                            "title": "Promotion",
                            "description": f"Promoted from {promotion[old_desig_field]} to {promotion[new_desig_field]}",
                            "type": "promotion",
                            "icon": "fa-award",
                        }
                    )
    except Exception as e:
        # Log the error but continue with other timeline items
        frappe.logger().error(f"Error fetching promotion data: {str(e)}")

    # Get additional salary entries
    try:
        additional_salaries = frappe.get_all(
            "Additional Salary",
            filters={"employee": employee_id},
            fields=["payroll_date", "salary_component", "amount", "type"],
            order_by="payroll_date asc",
        )

        # Add bonuses and additional compensations
        for additional in additional_salaries:
            title = "Bonus" if additional["type"] == "Earning" else "Deduction"
            timeline_events.append(
                {
                    "date": additional["payroll_date"],
                    "formatted_date": frappe.utils.formatdate(
                        additional["payroll_date"]
                    ),
                    "title": f"{title}: {additional['salary_component']}",
                    "description": f"Amount: {frappe.utils.fmt_money(additional['amount'])}",
                    "type": "additional_salary",
                    "icon": (
                        "fa-gift"
                        if additional["type"] == "Earning"
                        else "fa-minus-circle"
                    ),
                }
            )
    except Exception as e:
        # Log the error but continue with other timeline items
        frappe.logger().error(f"Error fetching additional salary data: {str(e)}")

    # Get leaves that might affect payroll
    try:
        leaves = frappe.get_all(
            "Leave Application",
            filters={
                "employee": employee_id,
                "status": "Approved",
                "leave_type": ["in", ["Unpaid Leave", "Medical Leave", "Sabbatical"]],
            },
            fields=["from_date", "to_date", "leave_type"],
            order_by="from_date asc",
        )

        # Add significant leaves to timeline
        for leave in leaves:
            timeline_events.append(
                {
                    "date": leave["from_date"],
                    "formatted_date": frappe.utils.formatdate(leave["from_date"]),
                    "title": f"{leave['leave_type']}",
                    "description": f"From {frappe.utils.formatdate(leave['from_date'])} to {frappe.utils.formatdate(leave['to_date'])}",
                    "type": "leave",
                    "icon": "fa-calendar-minus",
                }
            )
    except Exception as e:
        # Log the error but continue with other timeline items
        frappe.logger().error(f"Error fetching leave data: {str(e)}")

    # Sort all events by date
    sorted_events = sorted(timeline_events, key=lambda k: k["date"])

    return sorted_events
