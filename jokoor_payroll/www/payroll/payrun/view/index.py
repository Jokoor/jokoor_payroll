import frappe
from frappe.utils import getdate, date_diff, flt, cint
import pandas as pd
import io
import requests
from frappe import _


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/login?/dashboard/payrun"

    payrun_id = frappe.request.args.get("id")
    context.active_page = "payrun"
  

    payrun = frappe.get_doc("Payroll Entry", payrun_id)
    context.payrun = payrun
    context.payrun_date = getdate(payrun.posting_date)
    context.payrun_month_and_year = getdate(payrun.posting_date).strftime("%B %Y")
    context.payrun_day_only = getdate(payrun.posting_date).strftime("%d")
    context.payrun_days = date_diff(payrun.end_date, payrun.start_date)
    context.gross_pay = frappe.db.sql(
        f"""   
        SELECT SUM(gross_pay) FROM `tabSalary Slip` WHERE payroll_entry = '{payrun_id}'
    """
    )[0][0]
    context.net_pay = frappe.db.sql(
        f"""
        SELECT SUM(net_pay) FROM `tabSalary Slip` WHERE payroll_entry = '{payrun_id}'
    """
    )[0][0]

    # Fetch the employees in this pay run
    employees = []
    payslips = frappe.get_list(
        "Salary Slip",
        filters={"payroll_entry": payrun_id},
        fields=[
            "name",
            "employee",
            "employee_name",
            "department",
            "gross_pay",
            "net_pay",
            "status",
            "total_deduction",
            "end_date",
            "start_date",
        ],
    )
    for slip in payslips:
        paid_days = date_diff(slip.end_date, slip.start_date)
        sshfc_amount = frappe.db.get_value(
            "Salary Detail",
            {"parent": slip.name, "salary_component": "SSHFC"},
            "amount",
        )
        payee_amount = frappe.db.get_value(
            "Salary Detail", {"parent": slip.name, "salary_component": "PAYE"}, "amount"
        )
        employees.append(
            {
                "employee": frappe.db.get_value("Employee", slip.employee, "name"),
                "employee_name": slip.employee_name,
                "department": slip.department,
                "gross_pay": slip.gross_pay,
                "net_pay": slip.net_pay,
                "status": slip.status,
                "total_deduction": slip.total_deduction,
                "paid_days": paid_days,
                "sshfc_amount": sshfc_amount,
                "payee_amount": payee_amount,
                "name": slip.name,
            }
        )

    context.employees = employees

    context.taxes = get_taxes(payrun_id)
    context.payrun_status = get_payrun_status(payrun_id)

    # Fetch all earning and deduction components for the dropdowns
    context.earning_components = frappe.get_all(
        "Salary Component", filters={"type": "Earning"}, fields=["name"]
    )

    context.deduction_components = frappe.get_all(
        "Salary Component", filters={"type": "Deduction"}, fields=["name"]
    )

    return context


def get_employees(payrun_id):
    # get all salary slips with employee name gross pay net pay total deductions and also get the componet amount of payee and sshfc use joins to achive this
    salary_slips = frappe.get_all("Salary Slip", {"payroll_entry": payrun_id})
    data = []
    for slip in salary_slips:
        salary_slip = frappe.get_doc("Salary Slip", slip.name)
        sshfc_amount = frappe.db.get_value(
            "Salary Detail",
            {"parent": slip.name, "salary_component": "SSHFC"},
            "amount",
        )
        payee_amount = frappe.db.get_value(
            "Salary Detail", {"parent": slip.name, "salary_component": "PAYE"}, "amount"
        )
        data.append(

            {

                "employee_name": frappe.db.get_value(
                    "Employee", salary_slip.employee, "employee_name"
                ),
                "employee_id": frappe.db.get_value(
                    "Employee", salary_slip.employee, "name"
                ),
                "gross_pay": salary_slip.gross_pay,
                "net_pay": salary_slip.net_pay,
                "total_deduction": salary_slip.total_deduction,
                "sshfc_amount": sshfc_amount,
                "payee_amount": payee_amount,
                "paid_days": date_diff(salary_slip.end_date, salary_slip.start_date),
            }
        )
    return data


def get_taxes(payrun_id):
    salary_slips = frappe.get_all("Salary Slip", {"payroll_entry": payrun_id})
    sshfc_amount = 0
    payee_amount = 0
    for slip in salary_slips:
        salary_slip = frappe.get_doc("Salary Slip", slip.name)
        sshfc_amount += flt(
            frappe.db.get_value(
                "Salary Detail",
                {"parent": slip.name, "salary_component": "SSHFC"},
                "amount",
            )
        )
        payee_amount += flt(
            frappe.db.get_value(
                "Salary Detail",
                {"parent": slip.name, "salary_component": "PAYE"},
                "amount",
            )
        )

    return {
        "sshfc_amount": flt(sshfc_amount),
        "payee_amount": flt(payee_amount),
        "total_taxes": flt(sshfc_amount) + flt(payee_amount),
    }


def get_pre_tax_deductions(payrun_id):
    salary_slips = frappe.get_all("Salary Slip", {"payroll_entry": payrun_id})

    for slip in salary_slips:
        salary_slip = frappe.get_doc("Salary Slip", slip.name)
        for deduction in salary_slip.deductions:
            if deduction.salary_component not in ["PAYE", "SSHFC"]:
                pre_tax_deductions += flt(deduction.amount)
    return pre_tax_deductions


def get_payrun_status(payrun_id):

    draft_count = frappe.db.count(
        "Salary Slip", {"payroll_entry": payrun_id, "status": "Draft"}
    )
    submitted_count = frappe.db.count(
        "Salary Slip", {"payroll_entry": payrun_id, "status": "Submitted"}
    )
    all_count = frappe.db.count("Salary Slip", {"payroll_entry": payrun_id})
    if draft_count == all_count:
        return "Draft"
    elif submitted_count > 0:
        return "Processing"
    else:
        return "Completed"


@frappe.whitelist()
def update_salary_slip_component(slip_id, changes):
    """
    Update salary slip components with new amounts

    Args:
        slip_id (str): Salary Slip ID
        changes (list): List of changes to apply
    """
    try:
        if not frappe.has_permission("Salary Slip", "write"):
            return {"success": False, "error": "Insufficient permissions"}

        # Get the salary slip
        salary_slip = frappe.get_doc("Salary Slip", slip_id)

        # Check if slip is in draft status
        if salary_slip.docstatus != 0:  # 0 = Draft
            return {"success": False, "error": "Cannot edit a submitted salary slip"}

        # Process each change
        for change in changes:
            component = change.get("component")
            amount = flt(change.get("amount"))
            component_type = change.get("type")

            # Find and update the component
            components_list = (
                salary_slip.earnings
                if component_type == "earning"
                else salary_slip.deductions
            )
            component_found = False

            for comp in components_list:
                if comp.salary_component == component:
                    if comp.amount != amount:
                        comp.amount = amount
                        component_found = True
                    break

            if not component_found:
                return {"success": False, "error": f"Component {component} not found"}

        salary_slip.save()

        return {"success": True}

    except Exception as e:
        frappe.log_error(f"Error updating salary slip component: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def add_salary_slip_component(slip_id, component, type, amount):
    """
    Add a new component to a salary slip

    Args:
        slip_id (str): Salary Slip ID
        component (str): Component name
        type (str): 'earning' or 'deduction'
        amount (float): Component amount
    """
    try:
        if not frappe.has_permission("Salary Slip", "write"):
            return {"success": False, "error": "Insufficient permissions"}

        # Get the salary slip
        salary_slip = frappe.get_doc("Salary Slip", slip_id)

        # Check if slip is in draft status
        if salary_slip.docstatus != 0:  # 0 = Draft
            return {"success": False, "error": "Cannot edit a submitted salary slip"}

        # Check if component already exists
        components_list = (
            salary_slip.earnings if type == "earning" else salary_slip.deductions
        )
        for comp in components_list:
            if comp.salary_component == component:
                return {
                    "success": False,
                    "error": f"Component {component} already exists",
                }

        # Get abbreviation and other details from Salary Component
        component_doc = frappe.get_doc("Salary Component", component)

        # Add the new component
        row = salary_slip.append(
            "earnings" if type == "earning" else "deductions",
            {
                "salary_component": component,
                "abbr": component_doc.salary_component_abbr,
                "amount": flt(amount),
                "is_tax_applicable": (
                    component_doc.is_tax_applicable
                    if hasattr(component_doc, "is_tax_applicable")
                    else 0
                ),
            },
        )

        salary_slip.save()
        frappe.db.commit()

        return {"success": True}

    except Exception as e:
        frappe.log_error(f"Error adding salary slip component: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_available_components(type):
    """
    Get available salary components for the specified type

    Args:
        type (str): 'earning' or 'deduction'
    """
    try:
        # Set the proper condition based on type
        condition = "Earning" if type == "earning" else "Deduction"

        # Fetch active components
        components = frappe.get_all(
            "Salary Component",
            filters={"disabled": 0},
            or_filters={
                "type": condition,
            },
            fields=["name", "salary_component_abbr", "is_tax_applicable"],
        )

        return components

    except Exception as e:
        frappe.log_error(f"Error fetching available components: {str(e)}")
        return []


@frappe.whitelist()
def import_one_time_components(
    file_content=None, file_url=None, payrun_id=None, replace_existing=False
):
    """
    Import one-time components from a CSV file to employee salary slips.
    """
    try:
        if not payrun_id:
            return {"success": False, "message": "Payrun ID is required"}

        replace_existing = cint(replace_existing)

        # Get the CSV data
        try:
            if file_content:
                # Handle various file content formats
                if isinstance(file_content, str):
                    if file_content.startswith("data:"):
                        import base64

                        content_parts = file_content.split(",", 1)
                        if len(content_parts) > 1:
                            file_content = content_parts[1]
                            file_content = base64.b64decode(file_content).decode(
                                "utf-8"
                            )
                    csv_data = io.StringIO(file_content)
                else:
                    csv_data = io.StringIO(file_content.decode("utf-8"))
            elif file_url:
                response = requests.get(file_url)
                csv_data = io.StringIO(response.text)
            else:
                return {"success": False, "message": "No file content or URL provided"}

            # Read CSV data
            df = pd.read_csv(csv_data)
        except Exception as e:
            frappe.logger().error(f"Error reading CSV: {str(e)}")
            return {"success": False, "message": f"Failed to read CSV file: {str(e)}"}

        # Validate the CSV format
        if "Employee ID" not in df.columns:
            return {
                "success": False,
                "message": "CSV must contain 'Employee ID' column",
            }

        # Results tracking
        results = {"total": 0, "success": 0, "errors": 0, "details": []}
        success_details = []

        # Get all component columns (all except Employee ID)
        component_columns = [col for col in df.columns if col != "Employee ID"]
        if not component_columns:
            return {"success": False, "message": "No component columns found in CSV"}

        # Get all available components and their types
        available_components = {}
        for component in frappe.get_all("Salary Component", fields=["name", "type"]):
            available_components[component.name] = component.type

        # Process each row in the CSV
        for index, row in df.iterrows():
            employee_id = row["Employee ID"]
            if not employee_id or pd.isna(employee_id):
                continue  # Skip empty rows

            results["total"] += 1
            employee_result = {"employee_id": employee_id, "components_added": []}

            # Find the salary slip for this employee in the payrun
            salary_slips = frappe.get_all(
                "Salary Slip",
                filters={
                    "employee": employee_id,
                    "payroll_entry": payrun_id,
                    "docstatus": 0,  # Draft
                },
                fields=["name"],
            )

            if not salary_slips:
                results["errors"] += 1
                continue

            salary_slip_id = salary_slips[0].name
            has_updates = False

            # Process each component column
            for component_name in component_columns:
                component_amount = flt(row[component_name])
                if component_amount <= 0 or pd.isna(component_amount):
                    continue  # Skip zero, negative, or NaN amounts

                # Check if component exists
                if component_name not in available_components:
                    continue

                # Determine component type
                component_type = available_components[component_name]
                is_earning = component_type == "Earning"

                # Use direct SQL to check if the component exists
                component_exists = frappe.db.exists(
                    "Salary Detail",
                    {"parent": salary_slip_id, "salary_component": component_name},
                )

                # Update or add component using direct SQL
                if component_exists and replace_existing:
                    # Update existing component
                    frappe.db.set_value(
                        "Salary Detail",
                        {"parent": salary_slip_id, "salary_component": component_name},
                        "amount",
                        component_amount,
                    )
                    has_updates = True
                    employee_result["components_added"].append(
                        f"{component_name} (updated): GMD {component_amount}"
                    )
                elif not component_exists:
                    # Add new component
                    component_abbr = (
                        frappe.db.get_value(
                            "Salary Component", component_name, "salary_component_abbr"
                        )
                        or ""
                    )

                    # Insert directly into database
                    frappe.get_doc(
                        {
                            "doctype": "Salary Detail",
                            "parent": salary_slip_id,
                            "parentfield": "earnings" if is_earning else "deductions",
                            "parenttype": "Salary Slip",
                            "salary_component": component_name,
                            "abbr": component_abbr,
                            "amount": component_amount,
                            "is_one_time_component": 1,
                        }
                    ).insert(ignore_permissions=True)

                    has_updates = True
                    employee_result["components_added"].append(
                        f"{component_name} (added): GMD {component_amount}"
                    )

            # If components were added/updated, mark as success
            if has_updates:
                # Force recalculation of the salary slip
                salary_slip = frappe.get_doc("Salary Slip", salary_slip_id)
                salary_slip.run_method("calculate_net_pay")
                frappe.db.commit()

                results["success"] += 1
                success_details.append(
                    f"{employee_id}: {', '.join(employee_result['components_added'])}"
                )
            else:
                results["errors"] += 1

        # Commit all changes to database
        frappe.db.commit()

        # Return results
        return {
            "success": True,
            "message": f"Processed {results['total']} employees: {results['success']} successful, {results['errors']} errors",
            "details": success_details,
        }

    except Exception as e:
        frappe.logger().error(f"Unexpected error in import: {str(e)}")
        return {"success": False, "message": f"Import failed: {str(e)}"}


def get_salary_component_by_name(component_name):
    """
    Get salary component details by name
    """
    # First try exact match
    components = frappe.get_all(
        "Salary Component",
        filters={"name": component_name},
        fields=[
            "name",
            "salary_component_abbr",
            "is_tax_applicable",
            "type",  # This is the field we need
        ],
    )

    if components:
        # FIX: Log the component details to debug
        frappe.logger().info(
            f"Found component: {component_name}, type: {components[0].get('type')}"
        )
        return components[0]

    # Try case-insensitive match next
    components = frappe.get_all(
        "Salary Component",
        filters=[
            ["name", "like", f"%{component_name}%"]
        ],  # FIX: Improve the LIKE query
        fields=[
            "name",
            "salary_component_abbr",
            "is_tax_applicable",
            "type",
        ],
    )

    if components:
        # FIX: Log the component details to debug
        frappe.logger().info(
            f"Found component via LIKE: {component_name} → {components[0].name}, type: {components[0].get('type')}"
        )
        return components[0]

    # Log available components for debugging
    all_components = frappe.get_all("Salary Component", fields=["name", "type"])
    component_names = [f"{c.name} ({c.type})" for c in all_components]
    frappe.logger().info(f"Available components: {component_names}")
    frappe.logger().warning(f"Component not found: {component_name}")

    return None


@frappe.whitelist()
def get_template_sample():
    """
    Generate a sample template for one-time components

    Returns:
        dict: URL to download the template
    """
    from frappe.utils import get_site_url

    # Get earnings and deductions
    deductions = frappe.get_all(
        "Salary Component", {"type": "Deduction"}, ["component_name"]
    )
    earnings = frappe.get_all(
        "Salary Component", {"type": "Earning"}, ["component_name"]
    )

    # Create sample data
    template_url = f"{get_site_url()}/api/method/jokoor_payroll.www.dashboard.payrun.view.index.download_template"

    return {
        "success": True,
        "template_url": template_url,
        "sample_earnings": [comp.get("component_name") for comp in earnings[:5]],
        "sample_deductions": [comp.get("component_name") for comp in deductions[:5]],
    }


@frappe.whitelist()
def download_template():
    """
    Generate and download a template CSV for one-time components
    """
    from frappe.utils.response import build_response
    import csv

    # Get all employees for the sample
    employees = frappe.get_all("Employee", fields=["name as employee_id"], limit=5)

    # Get sample components to include in the template
    earnings = frappe.get_all(
        "Salary Component",
        filters={"type": "Earning", "disabled": 0},
        fields=["name"],
        limit=10,
    )

    deductions = frappe.get_all(
        "Salary Component",
        filters={"type": "Deduction", "disabled": 0},
        fields=["name"],
        limit=5,
    )

    # Create a sample CSV
    with io.StringIO() as sample_file:
        writer = csv.writer(sample_file)

        # Create headers: Employee ID followed by components
        headers = ["Employee ID"]

        # Add earnings first
        earning_names = [comp.get("name") for comp in earnings]
        headers.extend(earning_names)

        # Add deductions
        deduction_names = [comp.get("name") for comp in deductions]
        headers.extend(deduction_names)

        writer.writerow(headers)

        # Sample data rows with employees
        for employee in employees:
            # Create a row with employee ID and empty values for all components
            row = [employee.get("employee_id")] + [
                "" for _ in range(len(earning_names) + len(deduction_names))
            ]
            writer.writerow(row)

        # Add empty rows for users to fill
        for _ in range(5):
            row = [""] + ["" for _ in range(len(earning_names) + len(deduction_names))]
            writer.writerow(row)

        # Prepare the response
        frappe.response["filename"] = "one_time_components_template.csv"
        frappe.response["filecontent"] = sample_file.getvalue()
        frappe.response["type"] = "download"
        frappe.response["content_type"] = "text/csv"

        build_response("download")


@frappe.whitelist()
def debug_salary_slip_components(slip_id):
    """Debug function to check components in a salary slip"""
    try:
        if not frappe.has_permission("Salary Slip", "read"):
            return {"success": False, "error": "Insufficient permissions"}

        # Get the salary slip
        salary_slip = frappe.get_doc("Salary Slip", slip_id)

        # Extract components
        earnings = []
        for earning in salary_slip.earnings:
            earnings.append(
                {
                    "component": earning.salary_component,
                    "amount": earning.amount,
                    "is_one_time": earning.get("is_one_time_component", 0),
                }
            )

        deductions = []
        for deduction in salary_slip.deductions:
            deductions.append(
                {
                    "component": deduction.salary_component,
                    "amount": deduction.amount,
                    "is_one_time": deduction.get("is_one_time_component", 0),
                }
            )

        return {
            "success": True,
            "employee": salary_slip.employee_name,
            "earnings": earnings,
            "deductions": deductions,
            "gross_pay": salary_slip.gross_pay,
            "net_pay": salary_slip.net_pay,
        }

    except Exception as e:
        frappe.log_error(f"Error debugging salary slip: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def submit_payrun(payrun_id):
    """
    Submit all draft salary slips for a payrun

    Args:
        payrun_id (str): Payroll Entry ID

    Returns:
        dict: Result with success status and details
    """
    try:
        if not frappe.has_permission("Payroll Entry", "write"):
            return {
                "success": False,
                "message": "You don't have permission to submit this payrun",
            }

        # Get all draft salary slips for this payrun
        draft_slips = frappe.get_all(
            "Salary Slip",
            filters={"payroll_entry": payrun_id, "docstatus": 0},  # Draft
            fields=["name", "employee", "employee_name"],
        )

        if not draft_slips:
            return {
                "success": False,
                "message": "No draft salary slips found for this payrun",
            }

        # Count total, success and errors
        results = {
            "total": len(draft_slips),
            "success": 0,
            "errors": 0,
            "error_details": [],
        }

        # Submit each salary slip
        for slip in draft_slips:
            try:
                doc = frappe.get_doc("Salary Slip", slip.name)
                doc.submit()
                results["success"] += 1
            except Exception as e:
                results["errors"] += 1
                results["error_details"].append(
                    {
                        "employee": slip.employee_name,
                        "slip_id": slip.name,
                        "error": str(e),
                    }
                )
                frappe.log_error(f"Error submitting salary slip {slip.name}: {str(e)}")

        # Update payroll entry status if all slips were submitted
        if results["success"] == results["total"]:
            payrun_doc = frappe.get_doc("Payroll Entry", payrun_id)
            payrun_doc.set_status(update=True)

        # Commit all changes
        frappe.db.commit()

        return {
            "success": True,
            "message": f"Processed {results['total']} salary slips: {results['success']} submitted, {results['errors']} failed",
            "results": results,
        }

    except Exception as e:
        frappe.log_error(f"Error submitting payrun {payrun_id}: {str(e)}")
        return {"success": False, "message": f"Error submitting payrun: {str(e)}"}
