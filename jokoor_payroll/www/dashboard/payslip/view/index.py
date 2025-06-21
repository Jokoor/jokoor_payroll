import frappe
import json
from frappe import _


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/login?/dashboard/payslip"
        raise frappe.Redirect

    payslip_id = frappe.request.args.get("id")
    if not frappe.db.exists("Salary Slip", payslip_id):
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/404"
        raise frappe.Redirect

    context.payslip = frappe.get_doc("Salary Slip", payslip_id)
    context.employee = frappe.get_doc("Employee", context.payslip.employee)
    context.earning_components = frappe.get_all(
        "Salary Component",
        {"type": "Earning"},
        ["*"],
    )
    context.deduction_components = frappe.get_all(
        "Salary Component",
        {"type": "Deduction"},
        ["*"],
    )
    return context


@frappe.whitelist()
def update_payslip():
    """
    Update the payslip details from the submitted form data.
    Expected form structure:
    - payslip_id: ID of the payslip to update
    - status: New status (Draft/Submitted)
    - start_date: Pay period start date
    - end_date: Pay period end date
    - earnings: Array of earnings components
    - deductions: Array of deductions components
    """
    try:
        # Get form data
        form_data = frappe.request.form
        payslip_id = form_data.get("payslip_id")

        if not payslip_id:
            return {"success": False, "message": _("Payslip ID is required")}

        # Get the payslip document
        payslip = frappe.get_doc("Salary Slip", payslip_id)

        # Check if the payslip is in a state that can be updated
        if payslip.status != "Draft" and form_data.get("status") == "Draft":
            return {
                "success": False,
                "message": _("Only draft payslips can be updated"),
            }

        # Update basic payslip details
        payslip.start_date = form_data.get("start_date")
        payslip.end_date = form_data.get("end_date")

        # Process status change if requested
        new_status = form_data.get("status")
        if new_status and new_status != payslip.status:
            payslip.status = new_status

        # Process earnings components
        earnings_data = extract_component_data(form_data, "earnings")
        update_components(payslip, "earnings", earnings_data)

        # Process deductions components
        deductions_data = extract_component_data(form_data, "deductions")
        update_components(payslip, "deductions", deductions_data)

        # Calculate totals

        # Save the payslip
        payslip.save()

        # Submit if status changed to Submitted
        if new_status == "Submitted" and payslip.docstatus == 0:
            payslip.submit()
        frappe.db.commit()

        # Return success response
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/dashboard/payslip/view?id=" + payslip_id

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Payslip Update Error"))
        return {"success": False, "message": str(e)}


def extract_component_data(form_data, component_type):
    """
    Extract component data from the form submission.
    The form data structure uses array-like keys: earnings[0][salary_component], etc.
    """
    components = []
    prefix = f"{component_type}["

    # Find all relevant keys and extract the indices
    indices = set()
    for key in form_data:
        if key.startswith(prefix) and "][" in key:
            idx = key[len(prefix) : key.index("][")]
            if idx.isdigit():
                indices.add(int(idx))

    # For each index, build a component dictionary
    for idx in sorted(indices):
        component = {
            "salary_component": form_data.get(
                f"{component_type}[{idx}][salary_component]"
            ),
            "amount": float(form_data.get(f"{component_type}[{idx}][amount]", 0)),
            "idx": int(form_data.get(f"{component_type}[{idx}][idx]", idx + 1)),
        }

        # Handle is_tax_applicable (converting string value to boolean)
        tax_val = form_data.get(f"{component_type}[{idx}][is_tax_applicable]")
        component["is_tax_applicable"] = bool(int(tax_val)) if tax_val else False

        components.append(component)

    return components


def update_components(payslip, component_type, component_data):
    """
    Update the components in the payslip with the provided data.
    This handles adding, updating, and removing components.
    """
    # Get current components
    current_components = getattr(payslip, component_type)

    # Create a dictionary of existing components by name for easier lookup
    existing_components = {c.salary_component: c for c in current_components}

    # Track components to remove
    components_to_remove = []

    # First pass: Update existing components and mark which ones should be removed
    for i, component in enumerate(current_components):
        # Check if this component still exists in the updated data
        found = False
        for new_comp in component_data:
            if new_comp["salary_component"] == component.salary_component:
                # Update existing component
                component.amount = new_comp["amount"]
                component.is_tax_applicable = new_comp["is_tax_applicable"]
                component.idx = new_comp["idx"]
                found = True
                break

        # If not found in the updated data, mark for removal
        if not found:
            components_to_remove.append(component)

    # Remove components that are no longer present
    for component in components_to_remove:
        current_components.remove(component)

    # Second pass: Add new components
    for new_comp in component_data:
        if new_comp["salary_component"] not in existing_components:
            # Create a new component
            new_row = payslip.append(component_type, {})
            new_row.salary_component = new_comp["salary_component"]
            new_row.amount = new_comp["amount"]
            new_row.is_tax_applicable = new_comp["is_tax_applicable"]
            new_row.idx = new_comp["idx"]
