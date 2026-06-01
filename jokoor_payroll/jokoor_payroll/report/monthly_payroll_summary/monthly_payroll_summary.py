# Copyright (c) 2026, Jokoor and contributors
# For license information, please see license.txt

# Monthly Payroll Summary — one row per (month, company) showing:
#   - Headcount of unique employees with at least one Salary Slip in the month
#   - Total gross / total deductions / total net / total taxes
#
# Filters:
#   from_date, to_date — bracket months (inclusive of both endpoints)
#   company             — injected from the Payroll subscription context
#
# Citation: groups by YEAR/MONTH using start_date because Frappe Salary Slip
# rows don't carry an explicit `payroll_month` column. Submitted slips only
# (docstatus=1) so cancelled slips don't double-count.

import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": _("Year"), "fieldname": "year", "fieldtype": "Int", "width": 90},
		{"label": _("Month"), "fieldname": "month", "fieldtype": "Data", "width": 110},
		{"label": _("Headcount"), "fieldname": "headcount", "fieldtype": "Int", "width": 110},
		{"label": _("Total Gross"), "fieldname": "total_gross", "fieldtype": "Currency", "width": 150},
		{"label": _("Total Deductions"), "fieldname": "total_deductions", "fieldtype": "Currency", "width": 160},
		{"label": _("Total Taxes (PAYE)"), "fieldname": "total_paye", "fieldtype": "Currency", "width": 160},
		{"label": _("Total Net"), "fieldname": "total_net", "fieldtype": "Currency", "width": 150},
	]


def get_data(filters):
	conditions = ["ss.docstatus = 1"]
	values = {}

	company = filters.get("company")
	if company:
		conditions.append("ss.company = %(company)s")
		values["company"] = company

	from_date = filters.get("from_date")
	if from_date:
		conditions.append("ss.start_date >= %(from_date)s")
		values["from_date"] = from_date

	to_date = filters.get("to_date")
	if to_date:
		conditions.append("ss.end_date <= %(to_date)s")
		values["to_date"] = to_date

	where_clause = " AND ".join(conditions)

	# Aggregate Salary Slip totals per (year, month). PAYE deductions live in
	# `tabSalary Detail` rows so we LEFT JOIN to pull just that bucket per slip.
	# COALESCE so months with no PAYE component still surface.
	rows = frappe.db.sql(
		f"""
		SELECT
			YEAR(ss.start_date) as year,
			MONTHNAME(ss.start_date) as month,
			COUNT(DISTINCT ss.employee) as headcount,
			SUM(ss.gross_pay) as total_gross,
			SUM(ss.total_deduction) as total_deductions,
			COALESCE(SUM(paye.paye_amount), 0) as total_paye,
			SUM(ss.net_pay) as total_net
		FROM `tabSalary Slip` ss
		LEFT JOIN (
			SELECT parent, SUM(amount) as paye_amount
			FROM `tabSalary Detail`
			WHERE parenttype = 'Salary Slip' AND salary_component = 'PAYE'
			GROUP BY parent
		) paye ON paye.parent = ss.name
		WHERE {where_clause}
		GROUP BY YEAR(ss.start_date), MONTH(ss.start_date), MONTHNAME(ss.start_date)
		ORDER BY YEAR(ss.start_date) DESC, MONTH(ss.start_date) DESC
		""",
		values,
		as_dict=True,
	)

	return rows
