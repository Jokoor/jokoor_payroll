import frappe
from frappe import _
from frappe.utils import flt, getdate, date_diff


def get_context(context):
    """
    Prepare the context for the New Pay Run page
    """
    if frappe.session.user == "Guest":
        frappe.throw(
            _("You need to be logged in to access this page"), frappe.PermissionError
        )

    # Check permissions
    if not frappe.has_permission("Payroll Entry", "create"):
        frappe.throw(
            _("You don't have permission to create a Pay Run"), frappe.PermissionError
        )

    # Fetch employees
    context.employees = frappe.get_all(
        "Employee",
        filters={"status": "Active"},
        fields=[
            "name",
            "employee_name",
            "department",
            "designation",
            "branch",
            "grade",
        ],
    )

    # Fetch filter options
    context.branches = frappe.get_all("Branch", pluck="name")
    context.departments = frappe.get_all("Department", pluck="name")
    context.designations = frappe.get_all("Designation", pluck="name")
    context.grades = frappe.get_all("Employee Grade", pluck="name")

    # Set total count
    context.total_employees = len(context.employees)

    return context


def calculate_totals(salary_slip):
    """
    Calculate totals for the salary slip
    """
    # Initialize totals
    total_earnings = 0
    total_deductions = 0

    # Calculate total earnings
    for earning in salary_slip.earnings:
        total_earnings += flt(earning.amount)

    # Calculate total deductions
    for deduction in salary_slip.deductions:
        total_deductions += flt(deduction.amount)

    # Set gross and net pay
    salary_slip.gross_pay = total_earnings
    salary_slip.total_deduction = total_deductions
    salary_slip.net_pay = total_earnings - total_deductions

    return salary_slip


@frappe.whitelist()
def get_filtered_employees():
    """
    Get employees based on filter criteria
    """
    try:
        branch = frappe.form_dict.get("branch")
        department = frappe.form_dict.get("department")
        designation = frappe.form_dict.get("designation")
        grade = frappe.form_dict.get("grade")

        # Build filter criteria
        filters = {"status": "Active"}

        if branch:
            filters["branch"] = branch
        if department:
            filters["department"] = department
        if designation:
            filters["designation"] = designation
        if grade:
            filters["grade"] = grade

        # Get filtered employees
        employees = frappe.get_all(
            "Employee",
            filters=filters,
            fields=[
                "name",
                "employee_name",
                "department",
                "designation",
                "branch",
                "grade",
            ],
        )

        return {"success": True, "employees": employees, "count": len(employees)}

    except Exception as e:
        frappe.log_error(f"Error getting filtered employees: {str(e)}")
        return {"success": False, "message": str(e)}


def create_salary_slips(payroll_entry):
    """
    Create salary slips for all employees in the payroll entry
    """
    try:
        # Get employees from payroll entry
        employees = [employee.employee for employee in payroll_entry.employees]

        if not employees:
            frappe.throw(_("No employees found in the payroll entry"))

        company = payroll_entry.company
        start_date = payroll_entry.start_date
        end_date = payroll_entry.end_date
        posting_date = payroll_entry.posting_date

        # Create salary slips
        created_slips = []
        for employee_id in employees:
            # Check if salary slip already exists
            existing_slip = frappe.db.exists(
                "Salary Slip",
                {
                    "employee": employee_id,
                    "start_date": start_date,
                    "end_date": end_date,
                    "docstatus": ["<", 2],  # Not cancelled
                },
            )

            if existing_slip:
                created_slips.append(existing_slip)
                continue

            # Get employee details
            employee = frappe.get_doc("Employee", employee_id)

            # Get salary structure assignment
            salary_structure = get_salary_structure_assignment(
                employee_id, posting_date
            )

            if not salary_structure:
                frappe.logger().warning(
                    f"No salary structure found for employee {employee_id}"
                )
                continue

            # Create new salary slip
            salary_slip = frappe.new_doc("Salary Slip")
            salary_slip.employee = employee_id
            salary_slip.employee_name = employee.employee_name
            salary_slip.branch = employee.branch
            salary_slip.department = employee.department
            salary_slip.designation = employee.designation
            salary_slip.company = company
            salary_slip.posting_date = posting_date
            salary_slip.start_date = start_date
            salary_slip.end_date = end_date
            salary_slip.payroll_entry = payroll_entry.name

            # Set salary structure and calculate payment days
            salary_slip.salary_structure = salary_structure.salary_structure

            # Calculate payment days - should consider joining/relieving date and holidays
            payment_days = calculate_payment_days(
                employee_id,
                start_date,
                end_date,
                employee.date_of_joining,
                employee.relieving_date,
            )
            salary_slip.payment_days = payment_days

            # Set base amount from salary structure assignment
            salary_slip.base = salary_structure.base

            # Calculate working days
            total_working_days = date_diff(end_date, start_date) + 1
            salary_slip.total_working_days = total_working_days

            # Get earnings from salary structure
            structure_doc = frappe.get_doc(
                "Salary Structure", salary_structure.salary_structure
            )

            # Add earnings
            for earning in structure_doc.earnings:
                # Simplified for now - should use proper formula evaluation
                amount = calculate_component_amount(
                    earning, salary_structure.base, payment_days, total_working_days
                )

                salary_slip.append(
                    "earnings",
                    {
                        "salary_component": earning.salary_component,
                        "abbr": earning.abbr,
                        "amount": amount,
                        "is_tax_applicable": earning.is_tax_applicable or 0,
                    },
                )

            # Add deductions
            for deduction in structure_doc.deductions:
                # Simplified for now - should use proper formula evaluation
                amount = calculate_component_amount(
                    deduction, salary_structure.base, payment_days, total_working_days
                )

                salary_slip.append(
                    "deductions",
                    {
                        "salary_component": deduction.salary_component,
                        "abbr": deduction.abbr,
                        "amount": amount,
                    },
                )

            # Calculate totals
            salary_slip = calculate_totals(salary_slip)

            # Save the salary slip
            salary_slip.insert(ignore_permissions=True)
            created_slips.append(salary_slip.name)

            frappe.logger().info(
                f"Created salary slip {salary_slip.name} for employee {employee_id}"
            )

        # Update payroll entry with the created slips
        if created_slips:
            payroll_entry.db_set("salary_slips_created", 1)
            payroll_entry.db_set("status", "Draft")

            frappe.db.commit()

            frappe.logger().info(
                f"Created {len(created_slips)} salary slips for payroll entry {payroll_entry.name}"
            )

        return created_slips

    except Exception as e:
        frappe.log_error(f"Error creating salary slips: {str(e)}")
        frappe.throw(_("Error creating salary slips: {0}").format(str(e)))


def calculate_payment_days(
    employee_id, start_date, end_date, date_of_joining=None, relieving_date=None
):
    """
    Calculate payment days considering joining and relieving dates
    """
    payment_days = date_diff(end_date, start_date) + 1

    # Adjust for joining date
    if date_of_joining and getdate(date_of_joining) > getdate(start_date):
        payment_days -= date_diff(date_of_joining, start_date)

    # Adjust for relieving date
    if relieving_date and getdate(relieving_date) < getdate(end_date):
        payment_days -= date_diff(end_date, relieving_date)

    return payment_days


def calculate_component_amount(
    component, base_amount, payment_days, total_working_days
):
    """
    Calculate component amount based on formula or fixed amount
    """
    if component.amount_based_on_formula:
        try:
            # Simplified formula evaluation - in production should handle all variables
            formula = component.formula.replace("base", str(base_amount))
            amount = eval(formula)
        except Exception as e:
            frappe.logger().error(
                f"Error evaluating formula for component {component.salary_component}: {str(e)}"
            )
            amount = 0
    else:
        amount = component.amount

    # Pro-rate amount based on payment days
    if payment_days != total_working_days:
        amount = amount * flt(payment_days) / flt(total_working_days)

    return flt(amount, 2)


@frappe.whitelist()
def create_payrun():
    """
    Create a new payroll entry and generate salary slips
    """
    try:
        # Check permissions
        if not frappe.has_permission("Payroll Entry", "create"):
            frappe.throw(_("You don't have permission to create Payroll Entry"))

        # Get form data using a more robust approach
        form_data = frappe.local.form_dict

        # Debug what's being received
        frappe.logger().info(f"Received form data: {form_data}")

        payrun_name = form_data.get("payrun_name")
        payroll_frequency = form_data.get("payroll_frequency")
        start_date = form_data.get("start_date")
        end_date = form_data.get("end_date")
        posting_date = form_data.get("posting_date")
        base_days = form_data.get("base_days")

        # Get selected employees - handle different ways the form might submit employee data
        employees = []
        if form_data.get("employees[]"):
            # It might be a single value
            if isinstance(form_data.get("employees[]"), str):
                employees = [form_data.get("employees[]")]
            # Or it might be a list
            else:
                employees = form_data.get("employees[]")
        elif form_data.get("employees"):
            # Check if it's a comma-separated string
            if isinstance(form_data.get("employees"), str):
                employees = form_data.get("employees").split(",")
            else:
                employees = form_data.get("employees")

        # Log what we found
        frappe.logger().info(f"Found employees: {employees}")

        # Validate required fields
        if not (
            payrun_name
            and payroll_frequency
            and start_date
            and end_date
            and posting_date
            and base_days
        ):
            missing_fields = []
            if not payrun_name:
                missing_fields.append("Payrun Name")
            if not payroll_frequency:
                missing_fields.append("Payroll Frequency")
            if not start_date:
                missing_fields.append("Start Date")
            if not end_date:
                missing_fields.append("End Date")
            if not posting_date:
                missing_fields.append("Posting Date")
            if not base_days:
                missing_fields.append("Base Days")

            frappe.throw(
                _("Please fill all required fields: {0}").format(
                    ", ".join(missing_fields)
                )
            )

        if not employees:
            frappe.throw(_("Please select at least one employee"))
        company = frappe.db.get_value(
            "Company", frappe.db.get_value("User", frappe.session.user, "company")
        )
        company_abbr = frappe.db.get_value("Company", company, "abbr")

        # Create new Payroll Entry
        payroll_entry = frappe.new_doc("Payroll Entry")
        payroll_entry.payroll_frequency = payroll_frequency
        payroll_entry.company = company
        payroll_entry.payroll_payable_account = f"Payroll Payable - {company_abbr}"
        payroll_entry.start_date = start_date
        payroll_entry.end_date = end_date
        payroll_entry.posting_date = posting_date
        payroll_entry.exchange_rate = 1

        # Handle payrun naming - name field is auto-generated in most doctypes
        payroll_entry.payroll_name = payrun_name

        # Add employees to payroll entry
        for employee_id in employees:
            payroll_entry.append("employees", {"employee": employee_id})

        # Set additional fields
        payroll_entry.currency = frappe.db.get_value(
            "Company", payroll_entry.company, "default_currency"
        )

        # Save the payroll entry
        payroll_entry.save(ignore_permissions=True)
        frappe.db.commit()

        # Create salary slips
        salary_slips = create_salary_slips(payroll_entry)

        # Log success
        frappe.logger().info(
            f"Created payroll entry {payroll_entry.name} with {len(salary_slips)} salary slips"
        )

        # Return success response
        frappe.msgprint(
            _("Pay Run created successfully with {0} salary slips").format(
                len(salary_slips)
            )
        )

        # Redirect to the pay runs list page
        frappe.response["type"] = "redirect"
        frappe.response["location"] = "/dashboard/payrun"

    except Exception as e:
        frappe.log_error(f"Error creating pay run: {str(e)}")
        frappe.throw(_("Error creating pay run: {0}").format(str(e)))


def get_salary_structure_assignment(employee, date):
    """
    Get the salary structure assignment for an employee on the given date
    """
    assignment = frappe.db.get_value(
        "Salary Structure Assignment",
        {
            "employee": employee,
            "docstatus": 1,
            "from_date": ("<=", date),
            "to_date": (
                (">=", date)
                if frappe.db.has_column("Salary Structure Assignment", "to_date")
                else ("is", "not set")
            ),
        },
        ["salary_structure", "base"],
        as_dict=True,
    )

    if not assignment:
        # Try to get the latest assignment without an end date
        assignment = frappe.db.get_value(
            "Salary Structure Assignment",
            {
                "employee": employee,
                "docstatus": 1,
                "from_date": ("<=", date),
            },
            ["salary_structure", "base"],
            order_by="from_date desc",
            as_dict=True,
        )

    return assignment


@frappe.whitelist()
def check_existing_payslips():
    """
    Check if employees already have payslips in the given date range
    """
    try:
        # Get form data
        start_date = frappe.form_dict.get("start_date")
        end_date = frappe.form_dict.get("end_date")
        employees = frappe.form_dict.getlist("employees")

        # Handle single employee as string
        if not isinstance(employees, list) and employees:
            employees = [employees]

        if not (start_date and end_date and employees):
            return {
                "success": False,
                "message": "Missing required parameters",
                "existing_payslips": [],
            }

        # Check for overlapping payslips
        existing_payslips = []
        for employee in employees:
            # Check if any salary slip exists in the date range
            slips = frappe.get_all(
                "Salary Slip",
                filters={
                    "employee": employee,
                    "docstatus": ["!=", 2],  # Not cancelled
                    "start_date": ["<=", end_date],
                    "end_date": [">=", start_date],
                },
                fields=["name", "employee", "employee_name", "start_date", "end_date"],
            )

            if slips:
                for slip in slips:
                    existing_payslips.append(
                        {
                            "payslip": slip.name,
                            "employee": slip.employee,
                            "employee_name": slip.employee_name,
                            "period": f"{slip.start_date} to {slip.end_date}",
                        }
                    )

        return {
            "success": True,
            "message": f"Found {len(existing_payslips)} existing payslips in the date range",
            "existing_payslips": existing_payslips,
        }

    except Exception as e:
        frappe.log_error(f"Error checking existing payslips: {str(e)}")
        return {"success": False, "message": str(e), "existing_payslips": []}
