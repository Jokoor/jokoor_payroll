import frappe
from jokoor.utils import handle_login

def get_context(context):

    if handle_login("/payroll/adjustments"):
        context.active_page = 'adjustments'
        context.title = "Adjustments"
        context.subtitle = "Manage your adjustments"
        context.add_new_url = "/payroll/adjustment/new"

        if frappe.request.args.get("per_page"):
            per_page = int(frappe.request.args.get("per_page"))
        else:
            per_page = 20
        
        # Define table columns
        context.columns = [
            {"key": "name", "label": "Name"},
            {"key": "employee", "label": "Employee"},
            {"key": "salary_component", "label": "Salary Component"},
            {"key": "amount", "label": "Amount"},
            {"key": "is_recurring", "label": "Recurring"},
            {"key": "payroll_date", "label": "Payroll Date"},
        ]
        
        # Get employee data
        component_list = frappe.get_list(
            "Additional Salary", ["name", "employee", "salary_component", "amount", "is_recurring", "payroll_date"],
            limit=per_page
        )
        
        # Process employee data
        for component in component_list:
            doc = frappe.get_doc("Additional Salary", component.name)
            component.name = doc.name
            component.employee = doc.employee
            component.salary_component = doc.salary_component
            component.amount = doc.amount
            component.is_recurring = doc.is_recurring
            component.payroll_date = doc.payroll_date
           

            component.url = f"/payroll/adjustment/view?id={doc.name}"
           
        context.per_page = per_page 
        context.data = component_list
