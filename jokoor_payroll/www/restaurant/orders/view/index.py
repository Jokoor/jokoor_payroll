import frappe

def get_context(context):
    # Form settings
    context.form_id = "view-order"
    context.show_submit_button = False
    context.active_page = "orders"

    # Get order ID from URL
    context.order_id = frappe.form_dict.get('id', 'ORD-001')

    # Sample order data
    order_data = {
        "order_id": context.order_id,
        "customer_name": "John Doe",
        "table_no": "T1",
        "order_type": "dine_in",
        "guests": 2,
        "status": "Completed",
        "date": "2025-04-29",
        "time": "08:30 AM",
        "special_instructions": "No spicy food",
        "payment_method": "cash",
        "subtotal": "GMD 400.00",
        "tax": "GMD 50.00",
        "total": "GMD 450.00"
    }

    # Sample order items
    order_items = [
        {
            "item": "Chicken Biryani",
            "quantity": 2,
            "price": "GMD 150.00",
            "total": "GMD 300.00"
        },
        {
            "item": "Naan Bread",
            "quantity": 4,
            "price": "GMD 25.00",
            "total": "GMD 100.00"
        }
    ]

    # Define form sections and fields
    context.form_sections = [
        {
            "title": "Order Information",
            "icon": "fa-info-circle",
            "description": "Order details and status",
            "width": 6,
            "fields": [
                {
                    "type": "text",
                    "name": "order_id",
                    "label": "Order ID",
                    "value": order_data["order_id"],
                    "readonly": True,
                    "width": 6
                },
                {
                    "type": "text",
                    "name": "customer_name",
                    "label": "Customer Name",
                    "value": order_data["customer_name"],
                    "readonly": True,
                    "width": 6
                },
                {
                    "type": "text",
                    "name": "table_no",
                    "label": "Table Number",
                    "value": order_data["table_no"],
                    "readonly": True,
                    "width": 6
                },
                {
                    "type": "text",
                    "name": "order_type",
                    "label": "Order Type",
                    "value": order_data["order_type"].replace("_", " ").title(),
                    "readonly": True,
                    "width": 6
                },
                {
                    "type": "text",
                    "name": "status",
                    "label": "Status",
                    "value": order_data["status"],
                    "readonly": True,
                    "width": 6
                },
                {
                    "type": "text",
                    "name": "date",
                    "label": "Date",
                    "value": order_data["date"],
                    "readonly": True,
                    "width": 6
                },
                {
                    "type": "text",
                    "name": "time",
                    "label": "Time",
                    "value": order_data["time"],
                    "readonly": True,
                    "width": 6
                }
            ]
        },
        {
            "title": "Order Items",
            "icon": "fa-utensils",
            "description": "Items included in the order",
            "width": 12,
            "fields": [
                {
                    "type": "table",
                    "name": "order_items",
                    "label": "Items",
                    "readonly": True,
                    "columns": [
                        {"key": "item", "label": "Item"},
                        {"key": "quantity", "label": "Quantity"},
                        {"key": "price", "label": "Unit Price"},
                        {"key": "total", "label": "Total"}
                    ],
                    "data": order_items,
                    "width": 12
                }
            ]
        },
        {
            "title": "Additional Information",
            "icon": "fa-clipboard-list",
            "description": "Special instructions and payment details",
            "width": 6,
            "fields": [
                {
                    "type": "textarea",
                    "name": "special_instructions",
                    "label": "Special Instructions",
                    "value": order_data["special_instructions"],
                    "readonly": True,
                    "width": 12
                },
                {
                    "type": "text",
                    "name": "payment_method",
                    "label": "Payment Method",
                    "value": order_data["payment_method"].title(),
                    "readonly": True,
                    "width": 6
                },
                {
                    "type": "text",
                    "name": "subtotal",
                    "label": "Subtotal",
                    "value": order_data["subtotal"],
                    "readonly": True,
                    "width": 6
                },
                {
                    "type": "text",
                    "name": "tax",
                    "label": "Tax",
                    "value": order_data["tax"],
                    "readonly": True,
                    "width": 6
                },
                {
                    "type": "text",
                    "name": "total",
                    "label": "Total",
                    "value": order_data["total"],
                    "readonly": True,
                    "width": 6
                }
            ]
        }
    ]

    # Page settings
    context.page_title = f"Order {context.order_id}"
    context.page_description = "View order details"
    context.page_icon = "fa-file-alt"
    context.has_sidebar = True
    
    # Breadcrumb
    context.breadcrumb_items = [
        {"label": "Restaurant", "url": "/restaurant"},
        {"label": "Orders", "url": "/restaurant/orders"},
        {"label": context.order_id, "url": "#"}
    ]
