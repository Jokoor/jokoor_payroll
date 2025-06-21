import frappe

def get_context(context):
    # Page settings
    context.page_title = "Customers"
    context.page_description = "Manage restaurant customers"
    context.page_icon = "fa-users"
    context.has_sidebar = True
    context.active_page = "customers"
    
    # Breadcrumb
    context.breadcrumb_items = [
        {"label": "Restaurant", "url": "/restaurant"},
        {"label": "Customers", "url": "#"}
    ]

    # Pagination settings
    context.total_count = 5  # Total number of customers
    context.page_size = 10   # Items per page
    context.current_page = 1  # Current page number

    # Customer data
    context.data = [
        {
            "customer_id": "CUST-001",
            "name": "John Doe",
            "phone": "+220 7123 4567",
            "email": "john.doe@example.com",
            "total_orders": 15,
            "total_spent": "4500.00",
            "last_visit": "2025-04-28",
            "actions": [
                {"label": "View", "icon": "fa-eye", "url": "/restaurant/customers/view?id=CUST-001"},
                {"label": "Edit", "icon": "fa-edit", "url": "/restaurant/customers/edit?id=CUST-001"}
            ]
        },
        {
            "customer_id": "CUST-002",
            "name": "Jane Smith",
            "phone": "+220 7234 5678",
            "email": "jane.smith@example.com",
            "total_orders": 8,
            "total_spent": "2800.00",
            "last_visit": "2025-04-29",
            "actions": [
                {"label": "View", "icon": "fa-eye", "url": "/restaurant/customers/view?id=CUST-002"},
                {"label": "Edit", "icon": "fa-edit", "url": "/restaurant/customers/edit?id=CUST-002"}
            ]
        },
        {
            "customer_id": "CUST-003",
            "name": "Mike Johnson",
            "phone": "+220 7345 6789",
            "email": "mike.j@example.com",
            "total_orders": 12,
            "total_spent": "3600.00",
            "last_visit": "2025-04-27",
            "actions": [
                {"label": "View", "icon": "fa-eye", "url": "/restaurant/customers/view?id=CUST-003"},
                {"label": "Edit", "icon": "fa-edit", "url": "/restaurant/customers/edit?id=CUST-003"}
            ]
        },
        {
            "customer_id": "CUST-004",
            "name": "Sarah Williams",
            "phone": "+220 7456 7890",
            "email": "sarah.w@example.com",
            "total_orders": 20,
            "total_spent": "6000.00",
            "last_visit": "2025-04-29",
            "actions": [
                {"label": "View", "icon": "fa-eye", "url": "/restaurant/customers/view?id=CUST-004"},
                {"label": "Edit", "icon": "fa-edit", "url": "/restaurant/customers/edit?id=CUST-004"}
            ]
        },
        {
            "customer_id": "CUST-005",
            "name": "David Brown",
            "phone": "+220 7567 8901",
            "email": "david.b@example.com",
            "total_orders": 5,
            "total_spent": "1500.00",
            "last_visit": "2025-04-25",
            "actions": [
                {"label": "View", "icon": "fa-eye", "url": "/restaurant/customers/view?id=CUST-005"},
                {"label": "Edit", "icon": "fa-edit", "url": "/restaurant/customers/edit?id=CUST-005"}
            ]
        }
    ]
    
    return context
