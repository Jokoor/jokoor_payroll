# Copyright (c) 2026, Jokoor and contributors
# For license information, please see license.txt

# Headcount by Department — pivot of Active employees by department, with
# breakdown by employment_type and status. Useful for HR analytics and
# planning.
#
# Filters:
#   as_of   — optional ISO yyyy-mm-dd; defaults to today. Restricts to
#             employees joined on/before this date.
#   company — injected from the Payroll subscription context

import frappe
from frappe import _
from frappe.utils import today, getdate


def execute(filters=None):
	filters = filters or {}
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{"label": _("Department"), "fieldname": "department", "fieldtype": "Data", "width": 240},
		{"label": _("Active"), "fieldname": "active", "fieldtype": "Int", "width": 100},
		{"label": _("Inactive"), "fieldname": "inactive", "fieldtype": "Int", "width": 100},
		{"label": _("Suspended"), "fieldname": "suspended", "fieldtype": "Int", "width": 110},
		{"label": _("Left"), "fieldname": "left", "fieldtype": "Int", "width": 90},
		{"label": _("Full-time"), "fieldname": "full_time", "fieldtype": "Int", "width": 100},
		{"label": _("Part-time"), "fieldname": "part_time", "fieldtype": "Int", "width": 100},
		{"label": _("Contract"), "fieldname": "contract", "fieldtype": "Int", "width": 100},
		{"label": _("Probation"), "fieldname": "probation", "fieldtype": "Int", "width": 100},
		{"label": _("Total"), "fieldname": "total", "fieldtype": "Int", "width": 90},
	]


def get_data(filters):
	as_of = filters.get("as_of") or today()
	# Normalise + sanity-check
	try:
		as_of = getdate(as_of).isoformat()
	except Exception:
		as_of = today()

	conditions = ["(emp.date_of_joining IS NULL OR emp.date_of_joining <= %(as_of)s)"]
	values = {"as_of": as_of}

	if filters.get("company"):
		conditions.append("emp.company = %(company)s")
		values["company"] = filters["company"]

	where_clause = " AND ".join(conditions)

	rows = frappe.db.sql(
		f"""
		SELECT
			COALESCE(emp.department, 'Unassigned') as department,
			SUM(CASE WHEN emp.status = 'Active' THEN 1 ELSE 0 END) as active,
			SUM(CASE WHEN emp.status = 'Inactive' THEN 1 ELSE 0 END) as inactive,
			SUM(CASE WHEN emp.status = 'Suspended' THEN 1 ELSE 0 END) as suspended,
			SUM(CASE WHEN emp.status = 'Left' THEN 1 ELSE 0 END) as `left`,
			SUM(CASE WHEN emp.employment_type = 'Full-time' THEN 1 ELSE 0 END) as full_time,
			SUM(CASE WHEN emp.employment_type = 'Part-time' THEN 1 ELSE 0 END) as part_time,
			SUM(CASE WHEN emp.employment_type = 'Contract' THEN 1 ELSE 0 END) as contract,
			SUM(CASE WHEN emp.employment_type = 'Probation' THEN 1 ELSE 0 END) as probation,
			COUNT(*) as total
		FROM `tabEmployee` emp
		WHERE {where_clause}
		GROUP BY department
		ORDER BY total DESC, department
		""",
		values,
		as_dict=True,
	)

	# Strip the "- 6151F" company-suffix off department labels for display.
	for r in rows:
		d = r.get("department") or ""
		# Don't strip if there's no abbr suffix
		if " - " in d:
			r["department"] = d.split(" - ")[0]

	return rows
