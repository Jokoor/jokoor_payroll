

import frappe
import json

def get_context(context):
    context.active_page = "employees"
    context.title = "Employee"
    context.url = "employee"
    
    return context
    