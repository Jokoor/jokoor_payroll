import frappe

def get_context(context):
    # Common page settings
    context.page_title = "Orders"
    context.page_description = "View and manage restaurant orders"
    context.page_icon = "fa-shopping-cart"
    context.has_sidebar = True
    context.active_page = "orders"
    context.has_actions = True
    context.action_buttons = """
        <button class="btn btn-primary" onclick="window.location.href='/restaurant/orders/new'">
            <i class="fas fa-plus me-2"></i>New Order
        </button>
    """

    # Define breadcrumb 
    context.breadcrumb_items = [
        {"label": "Restaurant", "url": "/restaurant"},
        {"label": "Orders", "url": "#"}
    ]

    # Get page parameters
    page_size = int(frappe.form_dict.get('page_size', 10))
    page = int(frappe.form_dict.get('page', 1))
    
    # Calculate start and end for pagination
    start = (page - 1) * page_size

    # Table settings
    context.table_id = "orders-table"
    context.total_count = 10
    context.current_page = page
    context.page_size = page_size
    context.columns = [
        {"key": "order_id", "label": "Order ID", "sortable": True},
        {"key": "customer", "label": "Customer", "sortable": True},
        {"key": "table_no", "label": "Table", "sortable": True},
        {"key": "items", "label": "Items", "sortable": False},
        {"key": "total", "label": "Total", "sortable": True},
        {"key": "status", "label": "Status", "sortable": True},
        {"key": "date", "label": "Date", "sortable": True},
        {"key": "time", "label": "Time", "sortable": True}
    ]

    # Sample data
    context.data = [
        {
            "order_id": "ORD-001",
            "customer": "John Doe",
            "table_no": "T1",
            "items": "3 items",
            "total": "GMD 450.00",
            "status": "Completed",
            "date": "2025-04-29",
            "time": "08:30 AM"
        },
        {
            "order_id": "ORD-002",
            "customer": "Jane Smith",
            "table_no": "T4",
            "items": "2 items",
            "total": "GMD 275.00",
            "status": "In Progress",
            "date": "2025-04-29",
            "time": "08:45 AM"
        },
        {
            "order_id": "ORD-003",
            "customer": "Mike Johnson",
            "table_no": "T2",
            "items": "4 items",
            "total": "GMD 625.00",
            "status": "Pending",
            "date": "2025-04-29",
            "time": "09:00 AM"
        }
    ]

    # Common table settings
    context.has_search = True
    context.search_placeholder = "Search orders..."
    context.has_record_selector = True
    context.show_export = True
    context.show_actions = True
    context.delete_action = True
    context.delete_url = "/api/orders/delete"
    context.view_page = "/restaurant/orders/view/:id"
