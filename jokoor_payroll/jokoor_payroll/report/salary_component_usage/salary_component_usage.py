# Copyright (c) 2026, Jokoor and contributors
# For license information, please see license.txt

# Salary Component Usage — one row per Salary Component showing how many
# Salary Structures and how many distinct Employees (via Salary Structure
# Assignment) reference it.
#
# Filters:
#   company — injected from the Payroll subscription context

import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"label": _("Component"), "fieldname": "component", "fieldtype": "Link", "options": "Salary Component", "width": 240},
		{"label": _("Type"), "fieldname": "component_type", "fieldtype": "Data", "width": 110},
		{"label": _("Abbr"), "fieldname": "abbr", "fieldtype": "Data", "width": 80},
		{"label": _("# Structures"), "fieldname": "num_structures", "fieldtype": "Int", "width": 130},
		{"label": _("# Employees"), "fieldname": "num_employees", "fieldtype": "Int", "width": 130},
		{"label": _("Formula"), "fieldname": "formula", "fieldtype": "Data", "width": 280},
	]


def get_data(filters):
	company = filters.get("company")

	# Citation: Salary Detail rows are children of Salary Structure (template)
	# and of Salary Slip (run output) — we count the STRUCTURE references
	# because those are the configuration, not the runtime. Employee count
	# walks Salary Structure Assignment which carries the structure-employee
	# edge.
	company_clause = ""
	values = {}
	if company:
		company_clause = "AND ss.company = %(company)s"
		values["company"] = company

	rows = frappe.db.sql(
		f"""
		SELECT
			sc.name as component,
			sc.salary_component as component_label,
			sc.type as component_type,
			sc.salary_component_abbr as abbr,
			sc.formula as formula,
			COUNT(DISTINCT ss.name) as num_structures,
			COUNT(DISTINCT ssa.employee) as num_employees
		FROM `tabSalary Component` sc
		LEFT JOIN `tabSalary Detail` sd
			ON sd.salary_component = sc.salary_component
			AND sd.parenttype = 'Salary Structure'
		LEFT JOIN `tabSalary Structure` ss
			ON ss.name = sd.parent
			{company_clause}
		LEFT JOIN `tabSalary Structure Assignment` ssa
			ON ssa.salary_structure = ss.name
			AND ssa.docstatus = 1
		GROUP BY sc.name, sc.salary_component, sc.type, sc.salary_component_abbr, sc.formula
		ORDER BY num_employees DESC, num_structures DESC, sc.salary_component
		""",
		values,
		as_dict=True,
	)

	# Prefer the display label over the hash PK in the "component" cell — the
	# Link cell renders the PK anyway as a hint.
	for r in rows:
		if r.get("component_label"):
			r["component"] = r["component_label"]
		# Trim long formulas for display
		f = r.get("formula") or ""
		if len(f) > 120:
			r["formula"] = f[:117] + "..."

	return rows
