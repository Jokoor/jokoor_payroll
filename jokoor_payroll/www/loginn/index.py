import frappe


def get_context(context):
    context.no_cache = 1

    # If user is already logged in, redirect to dashboard
    if frappe.session.user != "Guest":
        frappe.local.flags.redirect_location = "/dashboard"
        raise frappe.Redirect

    # Set page title
    context.title = "Login | Jokoor Payroll"

    return context


@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    login_manager = frappe.auth.LoginManager()
    login_manager.authenticate(user=usr, pwd=pwd)
    login_manager.post_login()
    frappe.local.flags.redirect_location = "/dashboard"
    raise frappe.Redirect
