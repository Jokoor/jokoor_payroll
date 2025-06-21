import frappe
from frappe import _
# from jokoor.utils import check_login

def get_context(context):
    # Ensure user is logged in
    
    # Set page title and metadata
    context.page_title = "Reports"
    context.has_search = False
    context.has_actions = False
    
    # Define breadcrumb for navigation
    context.breadcrumb_items = [
        {"label": "Dashboard", "url": "/dashboard"},
        {"label": "Reports", "url": "#"}
    ]
    
    # Define the list of available reports
    context.reports = [
        {
            "title": "Salary Overview",
            "description": "View salary components (earnings and deductions) by employee or department",
            "icon": "fas fa-money-bill-wave",
            "url": "/dashboard/reports/salary-overview"
        },
        {
            "title": "Monthly Salary Report",
            "description": "View monthly salary details by employee or department",
            "icon": "fas fa-calendar-alt",
            "url": "/dashboard/reports/monthly-salary"
        }
    ]
    
    return context
