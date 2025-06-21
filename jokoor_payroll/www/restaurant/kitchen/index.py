import frappe

def get_context(context):
    # Page settings
    context.page_title = "Kitchen Display"
    context.page_description = "Manage kitchen orders and preparation"
    context.page_icon = "fa-utensils"
    context.has_sidebar = True
    context.active_page = "kitchen"
    
    # Define breadcrumb 
    context.breadcrumb_items = [
        {"label": "Restaurant", "url": "/restaurant"},
        {"label": "Kitchen", "url": "#"}
    ]

    # Sample orders data for different sections
    context.new_orders = [
        {
            "order_id": "ORD-001",
            "table": "T1",
            "time": "14:20",
            "items": [
                {"name": "Chicken Biryani", "quantity": 2, "notes": "Extra spicy"},
                {"name": "Naan Bread", "quantity": 4, "notes": ""}
            ],
            "customer": "John Doe",
            "status": "new"
        },
        {
            "order_id": "ORD-002",
            "table": "T4",
            "time": "14:15",
            "items": [
                {"name": "Butter Chicken", "quantity": 1, "notes": "No butter"},
                {"name": "Vegetable Curry", "quantity": 1, "notes": "Less spicy"}
            ],
            "customer": "Jane Smith",
            "status": "new"
        }
    ]

    context.in_progress_orders = [
        {
            "order_id": "ORD-003",
            "table": "T2",
            "time": "14:10",
            "items": [
                {"name": "Grilled Fish", "quantity": 2, "notes": "Well done"},
                {"name": "French Fries", "quantity": 1, "notes": "Extra crispy"}
            ],
            "customer": "Mike Johnson",
            "status": "cooking",
            "started_at": "14:12"
        }
    ]

    context.ready_orders = [
        {
            "order_id": "ORD-004",
            "table": "T3",
            "time": "14:05",
            "items": [
                {"name": "Caesar Salad", "quantity": 1, "notes": "No croutons"},
                {"name": "Club Sandwich", "quantity": 1, "notes": ""}
            ],
            "customer": "Sarah Williams",
            "status": "ready",
            "completed_at": "14:22"
        }
    ]

    # Kitchen stats
    context.kitchen_stats = {
        "new_orders": len(context.new_orders),
        "in_progress": len(context.in_progress_orders),
        "ready": len(context.ready_orders),
        "avg_prep_time": "18 mins",
        "total_orders_today": 45
    }
