import frappe
from jokoor.utils import handle_login

def get_context(context):

    if handle_login("/payroll/salary-structure"):
        context.active_page = 'salary-structure'
        context.title = "Salary Structures"
        context.subtitle = "Manage your salary structures"
        context.add_new_url = "/payroll/salary-structure/new"

        if frappe.request.args.get("per_page"):
            per_page = int(frappe.request.args.get("per_page"))
        else:
            per_page = 20
        
        # Define table columns
        context.columns = [
            {"key": "name", "label": "Name"},
            {"key": "is_active", "label": "Active"},
            {"key": "mode_of_payment", "label": "Mode of Payment"},
            {"key": "payroll_frequency", "label": "Payroll Frequency"},
        ]
        
        # Get employee data
        component_list = frappe.get_list(
            "Salary Structure", ["name", "is_active", "mode_of_payment", "payroll_frequency"],
            limit=per_page
        )
        
        # Process employee data
        for component in component_list:
            doc = frappe.get_doc("Salary Structure", component.name)
            component.name = doc.name
            component.is_active = doc.is_active
            component.mode_of_payment = doc.mode_of_payment
            component.payroll_frequency = doc.payroll_frequency
            if doc.is_active:
                component.status = "Active"
            else:
                component.status = "Inactive"

            component.url = f"/payroll/salary-structure/view?id={doc.name}"
            if doc.is_active:
                # inactive should be red
                component.status_html = '<span class="badge badge-success">Active</span>'
            else:
                # active should be green
                component.status_html = '<span class="badge badge-danger">Inactive</span>'
        
        context.per_page = per_page 
        context.data = component_list
