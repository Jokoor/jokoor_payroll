# Copyright (c) 2026, Jokoor and contributors
# For license information, please see license.txt

# Year-to-Date Earnings — per employee, sum the year's submitted Salary Slip
# totals (gross / deductions / PAYE / net). Useful for annual statements and
# tax filings.
#
# Filters:
#   year       — required (4-digit year, e.g. "2026")
#   employee   — optional Employee PK
#   department — optional Department PK
#   company    — injected from the Payroll subscription context

import frappe
from frappe import _
from frappe.utils import cstr


def execute(filters=None):
	filters = filters or {}
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"label": _("Employee"), "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 130},
		{"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 200},
		{"label": _("Department"), "fieldname": "department", "fieldtype": "Data", "width": 160},
		{"label": _("# Slips"), "fieldname": "num_slips", "fieldtype": "Int", "width": 80},
		{"label": _("YTD Gross"), "fieldname": "ytd_gross", "fieldtype": "Currency", "width": 150},
		{"label": _("YTD Deductions"), "fieldname": "ytd_deductions", "fieldtype": "Currency", "width": 160},
		{"label": _("YTD PAYE"), "fieldname": "ytd_paye", "fieldtype": "Currency", "width": 150},
		{"label": _("YTD Net"), "fieldname": "ytd_net", "fieldtype": "Currency", "width": 150},
	]


def get_data(filters):
	year = cstr(filters.get("year") or "")
	if not year or not year.isdigit() or len(year) != 4:
		frappe.throw(_("A 4-digit Year is required."))

	from_date = f"{year}-01-01"
	to_date = f"{year}-12-31"

	conditions = ["ss.docstatus = 1", "ss.start_date >= %(from_date)s", "ss.end_date <= %(to_date)s"]
	values = {"from_date": from_date, "to_date": to_date}

	if filters.get("company"):
		conditions.append("ss.company = %(company)s")
		values["company"] = filters["company"]

	if filters.get("employee"):
		conditions.append("ss.employee = %(employee)s")
		values["employee"] = filters["employee"]

	if filters.get("department"):
		conditions.append("emp.department = %(department)s")
		values["department"] = filters["department"]

	where_clause = " AND ".join(conditions)

	rows = frappe.db.sql(
		f"""
		SELECT
			ss.employee as employee,
			ss.employee_name as employee_name,
			emp.department as department,
			COUNT(ss.name) as num_slips,
			SUM(ss.gross_pay) as ytd_gross,
			SUM(ss.total_deduction) as ytd_deductions,
			COALESCE(SUM(paye.paye_amount), 0) as ytd_paye,
			SUM(ss.net_pay) as ytd_net
		FROM `tabSalary Slip` ss
		LEFT JOIN `tabEmployee` emp ON emp.name = ss.employee
		LEFT JOIN (
			SELECT parent, SUM(amount) as paye_amount
			FROM `tabSalary Detail`
			WHERE parenttype = 'Salary Slip' AND salary_component = 'PAYE'
			GROUP BY parent
		) paye ON paye.parent = ss.name
		WHERE {where_clause}
		GROUP BY ss.employee, ss.employee_name, emp.department
		ORDER BY ytd_gross DESC
		""",
		values,
		as_dict=True,
	)

	return rows
