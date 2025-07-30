import frappe
from jokoor.utils import handle_login

def get_context(context):
    if handle_login("/payroll/payslip"):
        context.active_page = 'payslip'
        context.title = "Payslip List"
        context.subtitle = "Manage your employee records"
        context.add_new_url = "/payroll/payslip/new"

        if frappe.request.args.get("per_page"):
            per_page = int(frappe.request.args.get("per_page"))
        else:
            per_page = 20
        
        # Define table columns
        context.columns = [
            {"key": "employee_id", "label": "Employee ID"},
            {"key": "employee_name", "label": "Employee Name"},
            {"key": "salary_structure", "label": "Salary Structure"},
            {"key": "gross_pay", "label": "Gross Pay"},
            {"key": "status_html", "label": "Status"}
        ]
        
        # Get employee data
        slip_list = frappe.get_list(
            "Salary Slip", 
            limit=per_page
        )
        
        # Process employee data
        for slip in slip_list:
            doc = frappe.get_doc("Salary Slip", slip.name)
            slip.employee_id = doc.employee
            slip.employee_name = doc.employee_name
            slip.salary_structure = doc.salary_structure
            slip.gross_pay = doc.gross_pay
            slip.url = f"/payroll/payslip/view?id={doc.name}"
            if doc.status == "Submitted":
                # submitted should be blue
                slip.status_html = '<span class="badge badge-secondary">Submitted</span>'
            elif doc.status == "Draft":
                # draft should be red
                slip.status_html = '<span class="badge badge-warning">Draft</span>'
        
        context.per_page = per_page 
        context.data = slip_list
