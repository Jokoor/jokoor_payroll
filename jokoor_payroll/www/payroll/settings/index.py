import frappe
import erpnext

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/login?/dashboard/settings"
        
    company = erpnext.get_default_company()
    context.company = frappe.get_doc("Company", company)
    context.salary_components = frappe.get_all("Salary Component", fields=["*"])