import frappe
from frappe import _
from datetime import datetime, timedelta

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
    
    # Get employee count
    context.employee_count = len(frappe.get_all("Employee", filters={"status": "Active"}))
    context.active_page = "dashboard"
    
    # Get recent pay runs
    recent_payruns = frappe.get_all(
        "Payroll Entry",
        ["name"],
        order_by="posting_date desc",
        limit=5
    )
    recent_payruns_list = []
    for payrun in recent_payruns:
        gross_pay = frappe.db.sql("""
            SELECT SUM(gross_pay) FROM `tabSalary Slip` WHERE payroll_entry = %s
        """, (payrun.name,))[0][0] or 0
        net_pay = frappe.db.sql("""
            SELECT SUM(net_pay) FROM `tabSalary Slip` WHERE payroll_entry = %s
        """, (payrun.name,))[0][0] or 0
        recent_payruns_list.append({
            "name": payrun.name,
            "posting_date": payrun.posting_date,
            "start_date": payrun.start_date,
            "end_date": payrun.end_date,
            "status": payrun.status,
            "gross_pay": gross_pay,
            "net_pay": net_pay
        })
        
    context.recent_payruns = recent_payruns_list
    
    # Process pay runs for employee count
    for payrun in recent_payruns:
        employee = frappe.get_all(
            "Salary Slip",
            {"payroll_entry": payrun.name},
            ["name", "employee"]
        )
        data = []
        for e in employee:
            data.append({
                "employee": e.employee,
                "employee_name": frappe.db.get_value("Employee", e.employee, "employee_name")
            })
        payrun["employees"] = data
    
    # Get total payrun count
    context.payrun_count = frappe.db.count("Payroll Entry")
    
  
    first_day_of_month = datetime.now().replace(day=1).date()
    if datetime.now().month == 12:
        first_day_of_next_month = datetime.now().replace(day=1, month=1, year=datetime.now().year + 1).date()
    else:
        first_day_of_next_month = datetime.now().replace(day=1, month=datetime.now().month + 1).date()
    last_day_of_month = first_day_of_next_month - timedelta(days=1)

    monthly_payroll = frappe.db.sql("""SELECT SUM(net_pay) as total
        FROM `tabSalary Slip`
        WHERE payroll_entry = %s
        AND posting_date BETWEEN %s AND %s
        AND docstatus = 1
        """, (
            payrun.name,  # This looks like it should be passed in too, though it's missing in original code
            first_day_of_month,
            last_day_of_month
        ))[0][0] or 0
    
    context.monthly_payroll = monthly_payroll
    context.avg_salary = monthly_payroll / context.employee_count if context.employee_count > 0 else 0
    
    # Get upcoming payruns
    upcoming_payruns = []
    for i in range(1, 4):  # Next 3 months
        next_month = datetime.now().replace(day=1) + timedelta(days=32 * i)
        next_month = next_month.replace(day=1)
        
        month_end = (next_month.replace(month=next_month.month + 1 if next_month.month < 12 else 1, 
                              year=next_month.year if next_month.month < 12 else next_month.year + 1) - 
                    timedelta(days=1))
        
        days_to_run = (next_month - datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)).days
        progress = max(0, min(100, 100 - (days_to_run / 30 * 100)))
        
        upcoming_payruns.append({
            "name": f"Monthly Payroll - {next_month.strftime('%B %Y')}",
            "start_date": next_month.strftime("%Y-%m-%d"),
            "end_date": month_end.strftime("%Y-%m-%d"),
            "days_to_run": days_to_run,
            "progress": progress
        })
    
    context.upcoming_payruns = upcoming_payruns
    
    # Get recent activities
    activities = []
    recent_logs = frappe.get_all(
        "Activity Log",
        filters={"operation": ["in", ["Login", "Logout", "Update", "Create"]]},
        fields=["user", "operation", "subject", "creation"],
        order_by="creation desc",
        limit=5
    )
    
    for log in recent_logs:
        activity_type = get_activity_type(log.operation)
        activities.append({
            "title": f"{log.user} {get_activity_text(log.operation)} {log.subject}",
            "time": frappe.utils.pretty_date(log.creation),
            "type": activity_type,
            "icon": get_activity_icon(log.operation)
        })
    
    context.recent_activities = activities
    
    # Get notifications
    notifications = []
    
    # Employees with birthday in the next 7 days
    today = datetime.now().date()
    upcoming_birthdays = frappe.db.sql("""
        SELECT name, employee_name, date_of_birth 
        FROM `tabEmployee` 
        WHERE 
            status = 'Active' AND
            MONTH(date_of_birth) = %s AND
            DAY(date_of_birth) BETWEEN %s AND %s
    """, (today.month, today.day, (today + timedelta(days=7)).day), as_dict=1)
    
    for employee in upcoming_birthdays:
        notifications.append({
            "title": f"{employee.employee_name}'s birthday on {employee.date_of_birth.strftime('%d %b')}",
            "time": f"{(employee.date_of_birth.replace(year=today.year) - today).days} days from now",
            "type": "primary"
        })
    
    # Employees about to hit work anniversaries
    upcoming_anniversaries = frappe.db.sql("""
        SELECT name, employee_name, date_of_joining 
        FROM `tabEmployee` 
        WHERE 
            status = 'Active' AND
            MONTH(date_of_joining) = %s AND
            DAY(date_of_joining) BETWEEN %s AND %s
    """, (today.month, today.day, (today + timedelta(days=7)).day), as_dict=1)
    
    for employee in upcoming_anniversaries:
        years = today.year - employee.date_of_joining.year
        if years > 0:
            notifications.append({
                "title": f"{employee.employee_name}'s {years} year work anniversary",
                "time": f"{(employee.date_of_joining.replace(year=today.year) - today).days} days from now",
                "type": "success"
            })
    
    # Payroll due soon
    if upcoming_payruns and upcoming_payruns[0]["days_to_run"] <= 7:
        notifications.append({
            "title": f"Payroll due in {upcoming_payruns[0]['days_to_run']} days",
            "time": f"{upcoming_payruns[0]['start_date']} to {upcoming_payruns[0]['end_date']}",
            "type": "warning"
        })
    
    context.notifications = notifications
    
    return context

def get_activity_type(operation):
    mapping = {
        "Login": "blue",
        "Logout": "orange",
        "Update": "green",
        "Create": "purple"
    }
    return mapping.get(operation, "purple")

def get_activity_icon(operation):
    mapping = {
        "Login": "sign-in-alt",
        "Logout": "sign-out-alt",
        "Update": "edit",
        "Create": "plus-circle"
    }
    return mapping.get(operation, "circle")

def get_activity_text(operation):
    mapping = {
        "Login": "logged in",
        "Logout": "logged out",
        "Update": "updated",
        "Create": "created"
    }
    return mapping.get(operation, "performed action on")