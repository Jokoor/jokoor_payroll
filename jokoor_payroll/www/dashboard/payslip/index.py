import frappe
from datetime import datetime
from frappe import _
from frappe.utils import getdate, flt, fmt_money


def get_context(context):
    """Prepare the context for the payslips page."""
    # Set page parameters
    context.page_title = "Payslips"
    context.page_description = "View and manage all payslips"
    context.page_icon = "fa-file-invoice-dollar"
    context.has_sidebar = True
    context.active_page = "payslips"
    context.has_actions = True
    context.action_buttons = """
        <button class="btn btn-primary" id="createPayslipBtn">
            <i class="fas fa-plus me-2"></i>Create Payslip
        </button>
    """
    
    # Define breadcrumb 
    context.breadcrumb_items = [
        {"label": "Dashboard", "url": "/dashboard"},
        {"label": "Payslips", "url": "#"}
    ]

    # Get pagination parameters
    page_size = int(frappe.form_dict.get('page_size', 20))
    page = int(frappe.form_dict.get('page', 1))
    month = frappe.form_dict.get('month', '')
    year = frappe.form_dict.get('year', '')
    status = frappe.form_dict.get('status', '')
    
    # Calculate start and end for pagination
    start = (page - 1) * page_size
    
    # Handle 'All' case
    if page_size == 0:  # 0 represents 'All'
        limit = None
    else:
        limit = page_size

    # Build filters
    filters = {}
    if month:
        filters['month'] = month
    if year:
        filters['year'] = year
    if status:
        filters['status'] = status

    # Get payslips with key details
    payslips = frappe.get_all(
        "Salary Slip",
        fields=[
            "name",
            "employee",
            "employee_name",
            "start_date",
            "end_date",
            "gross_pay",
            "total_deduction",
            "net_pay",
            "status",
            "creation"
        ],
        order_by="creation desc",
        start=start,
        limit=limit
    )

    # Format currency values
    for payslip in payslips:
        payslip.gross_pay = fmt_money(flt(payslip.gross_pay), 2, 'SAR')
        payslip.total_deduction = fmt_money(flt(payslip.total_deduction), 2, 'SAR')
        payslip.net_pay = fmt_money(flt(payslip.net_pay), 2, 'SAR')

    # Set up table columns
    context.columns = [
        {"key": "name", "label": "ID", "sortable": True},
        {"key": "employee_name", "label": "Employee", "sortable": True},
        {"key": "month", "label": "Month", "sortable": True},
        {"key": "year", "label": "Year", "sortable": True},
        {"key": "gross_pay", "label": "Gross Pay", "sortable": True, "align": "right"},
        {"key": "total_deduction", "label": "Deductions", "sortable": True, "align": "right"},
        {"key": "net_pay", "label": "Net Pay", "sortable": True, "align": "right"},
        {"key": "status", "label": "Status", "sortable": True, "type": "badge"}
    ]

    # Set up table data and pagination
    context.data = payslips
    context.total_count = frappe.db.count('Salary Slip', filters=filters)
    context.current_page = page
    context.page_size = page_size

    # Get summary statistics
    all_payslips = frappe.get_all(
        "Salary Slip",
        fields=["status", "net_pay", "start_date", "end_date"],
    )
    
    # Calculate summary metrics
    context.total_payslips = len(all_payslips)
    context.draft_payslips = len([p for p in all_payslips if p.status == "Draft"])
    context.submitted_payslips = len([p for p in all_payslips if p.status == "Submitted"])
    context.total_payout = fmt_money(
        sum(flt(p.net_pay) for p in all_payslips if p.status == "Submitted"),
        2,
        'SAR'
    )

    # Get current month's statistics
    current_month = datetime.now().month
    current_year = datetime.now().year
    context.current_month_payslips = 6

    return context