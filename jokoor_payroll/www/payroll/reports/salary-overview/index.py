import frappe
from frappe import _
from datetime import datetime

def get_context(context):
    # Ensure user is logged in
    
    # Get filter values from request
    employee = frappe.form_dict.get('employee', '')
    department = frappe.form_dict.get('department', '')
    start_date = frappe.form_dict.get('start_date', '')
    end_date = frappe.form_dict.get('end_date', '')
    
    # Set page title and metadata
    context.page_title = "Salary Overview"
    context.has_search = False
    context.has_actions = False
    
    # Define breadcrumb for navigation
    context.breadcrumb_items = [
        {"label": "Dashboard", "url": "/dashboard"},
        {"label": "Reports", "url": "/dashboard/reports"},
        {"label": "Salary Overview", "url": "#"}
    ]
    
    # Get the standardized report configuration
    context.report = get_report_config(employee, department, start_date, end_date)
    
    # Set month_year for display in the template header
    context.month_year = get_report_subtitle(start_date, end_date)
    
    return context

def get_report_config(employee=None, department=None, start_date=None, end_date=None):
    """
    Generate the complete report configuration
    Returns a dictionary with all necessary report components
    """
    # Get report data
    earnings, deductions, net_pay, sections = get_report_data(employee, department, start_date, end_date)
    
    # Prepare flat data as a fallback if sections are empty
    flat_data = []
    if earnings:
        flat_data.extend(earnings)
    if deductions:
        flat_data.extend(deductions)
    if net_pay:
        flat_data.append(net_pay)
    
    # Configure report
    return {
        'export_filename': f"Salary_Overview_Report_{datetime.now().strftime('%Y%m%d')}",
        'show_total': True,
        'currency_symbol': 'GMD',
        'filters': get_filter_options(employee, department, start_date, end_date),
        'columns': [
            {"key": "salary_component", "label": "Pay Components", "align": "center", "type": "data", "width": "250"},
            {"key": "amount", "label": "Amount (GMD)", "align": "center", "type": "number", "width": "150"}
        ],
        'sections': sections,
        'data': flat_data,  # Use flat data as a fallback if sections are empty
        'grand_total': net_pay,
        'freeze_columns': 0,
        'auto_submit': True
    }

def get_report_subtitle(start_date, end_date):
    """Generate a subtitle based on the date filters"""
    if start_date and end_date:
        start_formatted = frappe.utils.formatdate(start_date, "dd MMM yyyy")
        end_formatted = frappe.utils.formatdate(end_date, "dd MMM yyyy")
        return f"{start_formatted} to {end_formatted}"
    else:
        # Default to current year
        current_year = datetime.now().year
        return f"01 Jan {current_year} to 31 Dec {current_year}"

def get_filter_options(selected_employee, selected_department, start_date, end_date):
    """Get the filter configurations with options"""
    # Get employees for the filter dropdown
    employees = frappe.get_all("Employee", 
                              fields=["name", "employee_name"],
                              filters={"status": "Active"},
                              order_by="employee_name")
    
    employee_options = [{"value": emp.name, "label": f"{emp.employee_name} ({emp.name})"} for emp in employees]
    
    # Get departments for the filter dropdown
    departments = frappe.get_all("Department", 
                                fields=["name"],
                                order_by="name")
    
    department_options = [{"value": dept.name, "label": dept.name} for dept in departments]
    
    # Current year for default dates
    current_year = datetime.now().year
    default_start_date = start_date or f"{current_year}-01-01"
    default_end_date = end_date or f"{current_year}-12-31"
    return []
    
    return [
        {
            "name": "employee",
            "label": "Employee",
            "type": "select",
            "options": employee_options,
            "value": selected_employee,
            "column_size": 4
        },
        {
            "name": "department",
            "label": "Department",
            "type": "select",
            "options": department_options,
            "value": selected_department,
            "column_size": 4
        },
        {
            "name": "start_date",
            "label": "Start Date",
            "type": "date",
            "value": default_start_date,
            "column_size": 2
        },
        {
            "name": "end_date",
            "label": "End Date",
            "type": "date",
            "value": default_end_date,
            "column_size": 2
        }
    ]

def get_report_data(employee=None, department=None, start_date=None, end_date=None):
    """
    Get all salary component data and organize it into sections for the report
    Returns:
        - earnings: list of earning components
        - deductions: list of deduction components
        - net_pay: net pay calculation
        - sections: structured sections for the report_table component
    """
    # Build filters for the query
    conditions = ["ss.docstatus = 1"]
    
    if employee:
        conditions.append(f"ss.employee = '{employee}'")
    
    if department:
        conditions.append(f"ss.department = '{department}'")
    
    if start_date:
        conditions.append(f"ss.start_date >= '{start_date}'")
    
    if end_date:
        conditions.append(f"ss.end_date <= '{end_date}'")
    
    where_clause = " AND ".join(conditions)
    
    # Use SQL query to get salary components and their values
    query = f"""
        SELECT 
            sd.salary_component, 
            SUM(sd.amount) as amount,
            sc.type as component_type
        FROM 
            `tabSalary Detail` sd
        INNER JOIN 
            `tabSalary Slip` ss ON sd.parent = ss.name
        LEFT JOIN
            `tabSalary Component` sc ON sd.salary_component = sc.name
        WHERE 
            {where_clause}
        GROUP BY 
            sd.salary_component, sc.type
        ORDER BY 
            sc.type, sd.salary_component
    """
    
    results = frappe.db.sql(query, as_dict=True)
    
    # Separate components by type and calculate totals
    earnings = []
    deductions = []
    total_earnings = 0
    total_deductions = 0
    
    for item in results:
        amount = item.amount or 0
        component_type = item.component_type or "Earning"  # Default to Earning if type is not set
        
        if component_type.lower() == "earning":
            earnings.append({
                "salary_component": item.salary_component,
                "amount": f"GMD {amount:,.2f}"
            })
            total_earnings += amount
        else:
            deductions.append({
                "salary_component": item.salary_component,
                "amount": f"GMD {amount:,.2f}"
            })
            total_deductions += amount
    
    # Add totals for earnings and deductions
    if earnings:
        earnings.append({
            "salary_component": "Total Earnings",
            "amount": f"GMD {total_earnings:,.2f}",
            "is_total": True
        })
    
    if deductions:
        deductions.append({
            "salary_component": "Total Deductions",
            "amount": f"GMD {total_deductions:,.2f}",
            "is_total": True
        })
    
    # Calculate net pay
    net_pay = {
        "salary_component": "Net Pay",
        "amount": f"GMD {(total_earnings - total_deductions):,.2f}",
        "is_total": True
    }
    
    # Create structured sections for the report_table component
    sections = [
        {
            "title": "Earnings",
            "data": earnings,
            "has_total": True,
            "total_label": "Total Earnings"
        },
        {
            "title": "Deductions",
            "data": deductions,
            "has_total": True,
            "total_label": "Total Deductions"
        }
    ]
    
    return earnings, deductions, net_pay, sections