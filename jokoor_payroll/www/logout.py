import frappe


def get_context(context):
    redirect_to = frappe.form_dict.get("redirect-to") or frappe.request.args.get(
        "redirect-to"
    )

    # Set the redirect URL for the login page
    if redirect_to:
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = f"/login?redirect-to={redirect_to}"
        raise frappe.Redirect

    # Default logout behavior
    frappe.local.login_manager.logout()
    frappe.db.commit()

    context.title = "Logged Out"
