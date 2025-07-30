import frappe
def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/login?redirect=/payroll/payrun"
    context.active_page = 'payrun'
    context.title = "Payrun List"
    context.subtitle = "Manage your employee records"
    payrun_list = frappe.get_all("Payroll Entry", {"status": "Submitted"}, ["name", "posting_date"])
    all_payrun_list = []
    for payrun in payrun_list:
        gross_pay = frappe.db.sql("""
            SELECT SUM(gross_pay) FROM `tabSalary Slip` WHERE payroll_entry = %s
        """, (payrun.name,))
        net_pay = frappe.db.sql("""
            SELECT SUM(net_pay) FROM `tabSalary Slip` WHERE payroll_entry = %s
        """, (payrun.name,))
        all_payrun_list.append({
            "name": payrun.name,
            "employees":frappe.db.get_list("Salary Slip", filters={"payroll_entry": payrun.name}),
            "posting_date": payrun.posting_date,
            "status": get_payrun_status(payrun.name),
            "gross_pay": gross_pay[0][0],
            "net_pay": net_pay[0][0]
        })
    context.payrun_list = all_payrun_list
    return context
        

def get_payrun_status(payrun_id):
   
    draft_count = frappe.db.count("Salary Slip", {"payroll_entry": payrun_id, "status": "Draft"})
    submitted_count = frappe.db.count("Salary Slip", {"payroll_entry": payrun_id, "status": "Submitted"})
    all_count = frappe.db.count("Salary Slip", {"payroll_entry": payrun_id})
    if draft_count == all_count:
        return "Draft"
    elif submitted_count == all_count:
        return "Completed"
    else:
        return "Processing"