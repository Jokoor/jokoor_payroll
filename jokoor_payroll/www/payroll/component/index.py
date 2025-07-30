import frappe
from jokoor.utils import handle_login

def get_context(context):

    if handle_login("/payroll/component"):
        context.active_page = 'component'
        context.title = "Salary Components"
        context.subtitle = "Manage your salary components"
        context.add_new_url = "/payroll/component/new"

        if frappe.request.args.get("per_page"):
            per_page = int(frappe.request.args.get("per_page"))
        else:
            per_page = 20
        
        # Define table columns
        context.columns = [
            {"key": "name", "label": "Name"},
            {"key": "salary_component_abbr", "label": "Abbreviation"},
            {"key": "type", "label": "Type"},
            {"key": "status_html", "label": "Status"},
            {"key": "creation", "label": "Created At"}
        ]
        
        # Get employee data
        component_list = frappe.get_list(
            "Salary Component", ["name", "salary_component_abbr", "type", "disabled", "creation"],
            limit=per_page
        )
        
        # Process employee data
        for component in component_list:

            doc = frappe.get_doc("Salary Component", component.name)
            creation = frappe.utils.format_date(doc.creation, "dd-MMM-yyyy")
            component.creation = creation
            component.name = doc.name
            component.salary_component_abbr = doc.salary_component_abbr
            component.type = doc.type
            if doc.disabled:
                component.status = "Inactive"
            else:
                component.status = "Active"

            component.url = f"/payroll/component/view?id={doc.name}"
            if doc.disabled:
                # inactive should be red
                component.status_html = '<span class="badge badge-danger">Inactive</span>'
            else:
                # active should be green
                component.status_html = '<span class="badge badge-success">Active</span>'
        
        context.per_page = per_page 
        context.data = component_list
