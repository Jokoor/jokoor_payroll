import frappe

def get_context(context):
    # Form settings
    context.form_id = "new-order"
    context.form_action = "/api/orders/create"
    context.form_method = "POST"
    context.show_submit_button = True
    context.submit_button_text = "Create Order"
    context.form_validate = True
    context.active_page = "orders"

    # Define form sections and fields
    context.form_sections = [
        {
            "title": "Order Information",
            "icon": "fa-info-circle",
            "description": "Enter the basic details of the order",
            "width": 6,
            "fields": [
                {
                    "type": "text",
                    "name": "customer_name",
                    "label": "Customer Name",
                    "required": True,
                    "placeholder": "Enter customer name",
                    "width": 6
                },
                {
                    "type": "select",
                    "name": "table_no",
                    "label": "Table Number",
                    "required": True,
                    "options": [
                        {"value": "T1", "label": "Table 1"},
                        {"value": "T2", "label": "Table 2"},
                        {"value": "T3", "label": "Table 3"},
                        {"value": "T4", "label": "Table 4"},
                        {"value": "T5", "label": "Table 5"}
                    ],
                    "width": 6
                },
                {
                    "type": "select",
                    "name": "order_type",
                    "label": "Order Type",
                    "required": True,
                    "options": [
                        {"value": "dine_in", "label": "Dine In"},
                        {"value": "takeaway", "label": "Takeaway"},
                        {"value": "delivery", "label": "Delivery"}
                    ],
                    "width": 6
                },
                {
                    "type": "number",
                    "name": "guests",
                    "label": "Number of Guests",
                    "required": True,
                    "min": 1,
                    "default": 1,
                    "width": 6
                }
            ]
        },
        {
            "title": "Order Items",
            "icon": "fa-utensils",
            "description": "Select items for the order",
            "width": 12,
            "fields": [
                {
                    "type": "table",
                    "name": "order_items",
                    "label": "Items",
                    "required": True,
                    "columns": [
                        {"key": "item", "label": "Item", "type": "select", "options": [
                            {"value": "item1", "label": "Chicken Biryani"},
                            {"value": "item2", "label": "Butter Chicken"},
                            {"value": "item3", "label": "Vegetable Curry"},
                            {"value": "item4", "label": "Naan Bread"}
                        ]},
                        {"key": "quantity", "label": "Quantity", "type": "number", "min": 1},
                        {"key": "price", "label": "Unit Price", "type": "currency", "readonly": True},
                        {"key": "total", "label": "Total", "type": "currency", "readonly": True}
                    ],
                    "add_row": True,
                    "delete_row": True,
                    "width": 12
                }
            ]
        },
        {
            "title": "Additional Information",
            "icon": "fa-clipboard-list",
            "description": "Add any special instructions or notes",
            "width": 6,
            "fields": [
                {
                    "type": "textarea",
                    "name": "special_instructions",
                    "label": "Special Instructions",
                    "placeholder": "Enter any special instructions or dietary requirements",
                    "width": 12
                },
                {
                    "type": "select",
                    "name": "payment_method",
                    "label": "Payment Method",
                    "required": True,
                    "options": [
                        {"value": "cash", "label": "Cash"},
                        {"value": "card", "label": "Card"},
                        {"value": "mobile", "label": "Mobile Money"}
                    ],
                    "width": 6
                }
            ]
        }
    ]

    # Page settings
    context.page_title = "New Order"
    context.page_description = "Create a new restaurant order"
    context.page_icon = "fa-plus"
    context.has_sidebar = True
    
    # Breadcrumb
    context.breadcrumb_items = [
        {"label": "Restaurant", "url": "/restaurant"},
        {"label": "Orders", "url": "/restaurant/orders"},
        {"label": "New Order", "url": "#"}
    ]
