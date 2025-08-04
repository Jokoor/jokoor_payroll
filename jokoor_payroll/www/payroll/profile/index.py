import frappe

def get_context(context):
    # Get employee ID from URL
    user_id = frappe.session.user
    context.user_id = user_id
    context.active_page = "settings"
    context.title = "Profile"
    context.url = f"user-profile/{user_id}"
    context.is_editable = True
    context.image = frappe.utils.get_url(frappe.db.get_value("Employee", user_id, "image"))
    return context
    