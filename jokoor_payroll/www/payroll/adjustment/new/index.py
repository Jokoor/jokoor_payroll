

import frappe
import json

def get_context(context):
    context.active_page = "adjustments"
    context.title = "New Additional Salary"
    context.subtitle = "Create a new additional salary"
    