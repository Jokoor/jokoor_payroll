import frappe

def login_redirect(login_manager):
    """
    Redirects user to the page they were on before logging out
    or to a role-specific default page if no redirect is specified
    """
    # Check if there's a redirect URL in the form
    redirect_to = frappe.form_dict.get("redirect-to")
    
    # If we have a valid redirect path, use it
    if redirect_to and not redirect_to.startswith(('http://', 'https://')):
        frappe.local.response["redirect_to"] = redirect_to
        return
    
    # Otherwise, fall back to role-based defaults
    user = frappe.session.user
    roles = frappe.get_roles(user)
    
    if "Employee" in roles:
        frappe.local.response["redirect_to"] = "/dashboard/employee"
    elif "HR Manager" in roles:
        frappe.local.response["redirect_to"] = "/dashboard/hr"
    else:
        frappe.local.response["redirect_to"] = "/dashboard"

# Keep this function for backward compatibility
def after_login(login_manager):
    login_redirect(login_manager)
