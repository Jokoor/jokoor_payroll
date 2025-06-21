import frappe
import json

def get_context(context):
    context.update({
        "form_title": "Restaurant Invoice",
        "form_description": "Create a new invoice for your restaurant",
        "submit_url": "/api/method/jokoor_payroll.api.restaurant.save_invoice",
        "cancel_url": "/restaurant/list"
    })

    # Debug output
    print("Loading form fields...")

    # Basic Information
    context.fields = [
        {
            "type": "text",
            "name": "invoice_number",
            "label": "Invoice Number",
            "required": True,
            "width": 4,
            "placeholder": "Enter invoice number"
        },
        {
            "type": "date",
            "name": "invoice_date",
            "label": "Invoice Date",
            "required": True,
            "width": 4,
            "value": frappe.utils.today(),
            "min": "2020-01-01",
            "max": "2030-12-31"
        },
        {
            "type": "select",
            "name": "customer",
            "label": "Customer",
            "required": True,
            "width": 4,
            "placeholder": "Select a customer",
            "options": [
                {"value": "1", "label": "John Doe"},
                {"value": "2", "label": "Jane Smith"},
                {"value": "3", "label": "Bob Johnson"}
            ]
        },
        {
            "type": "table",
            "name": "items",
            "label": "Invoice Items",
            "required": True,
            "width": 12,
            "columns": [
                {
                    "name": "item",
                    "label": "Item",
                    "type": "select",
                    "options": [
                        {"value": "1", "label": "Item 1"},
                        {"value": "2", "label": "Item 2"},
                        {"value": "3", "label": "Item 3"}
                    ],
                    "required": True,
                    "placeholder": "Enter item name"
                },
                
               
                {
                    "name": "price",
                    "label": "Unit Price",
                    "type": "number",
                    "required": True,
                    "min": 0,
                    "step": 0.01,
                    "placeholder": "Enter price"
                },
                {
                    "name": "total",
                    "label": "Total",
                    "type": "number",
                    "readonly": True,
                    "step": 0.01
                }
            ],
            "show_summary": True,
            "summary": [
                {
                    "name": "subtotal",
                    "label": "Subtotal"
                },
                {
                    "name": "tax",
                    "label": "Tax (10%)"
                },
                {
                    "name": "total",
                    "label": "Total"
                }
            ],
            "value": [
                {
                    "item": "Pizza Margherita",
                    "description": "Classic Italian pizza",
                    "quantity": 2,
                    "price": 12.99,
                    "total": 25.98
                }
            ]
        },
        {
            "type": "textarea",
            "name": "notes",
            "label": "Notes",
            "width": 12,
            "placeholder": "Enter any additional notes"
        },
        
    ]

    # Debug output
    print("Form fields loaded:")
    for field in context.fields:
        if field["type"] == "table":
            print(f"Table field '{field['name']}' columns:", json.dumps(field["columns"]))
            print(f"Table field '{field['name']}' value:", json.dumps(field["value"]))

    # Action Buttons
    # context.action_buttons = [
    #     {
    #         "label": "Print Invoice",
    #         "icon": "fas fa-print",
    #         "class": "jk-btn-info",
    #         "action": "print",
    #         "url": "/api/method/jokoor_payroll.api.restaurant.print_invoice",
    #         "position": "left"
    #     },
    #     {
    #         "label": "Save & Send",
    #         "icon": "fas fa-paper-plane",
    #         "class": "jk-btn-success",
    #         "action": "submit",
    #         "url": "/api/method/jokoor_payroll.api.restaurant.send_invoice",
    #         "position": "right"
    #     },
    #     {
    #         "label": "Save Draft",
    #         "icon": "fas fa-save",
    #         "class": "jk-btn-secondary",
    #         "action": "save",
    #         "url": "/api/method/jokoor_payroll.api.restaurant.save_draft",
    #         "position": "right"
    #     }
    # ]

    return context