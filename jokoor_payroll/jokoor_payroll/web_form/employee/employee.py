import frappe

def get_context(context):
	if frappe.session.user == "Guest":
		frappe.redirect("/login")
	# take the full path of the url 
	url = frappe.request.headers.get("Referer")
	if not url:
		frappe.redirect("/payroll/employees")
	context.id = frappe.request.args.get("id")
	return context