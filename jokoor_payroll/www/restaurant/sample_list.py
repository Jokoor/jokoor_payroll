import frappe

def get_context(context):
    context.title = "Sample List"
    context.subtitle = "Manage your sample records"
    context.add_new_url = "/restaurant/sample"
    
    # Define table columns
    context.columns = [
        {"key": "invoice_number", "label": "Invoice Number"},
        {"key": "invoice_date", "label": "Date"},
        {"key": "customer", "label": "Customer"},
        {"key": "total", "label": "Total"},
        {"key": "status_html", "label": "Status"}
    ]
    
    # Sample data for the table
    context.data = [
        {
            "id": 1,
            "invoice_number": "INV-001",
            "invoice_date": "2025-04-30",
            "customer": "John Doe",
            "total": "$150.00",
            "status": "Active",
            "status_html": '<span class="badge badge-success">Active</span>',
            "url": "/restaurant/sample?id=1"
        },
        {
            "id": 2,
            "invoice_number": "INV-002",
            "invoice_date": "2025-04-29",
            "customer": "Jane Smith",
            "total": "$75.50",
            "status": "Pending",
            "status_html": '<span class="badge badge-warning">Pending</span>',
            "url": "/restaurant/sample?id=2"
        },
        {
            "id": 3,
            "invoice_number": "INV-003",
            "invoice_date": "2025-04-28",
            "customer": "Bob Wilson",
            "total": "$220.00",
            "status": "Inactive",
            "status_html": '<span class="badge badge-danger">Inactive</span>',
            "url": "/restaurant/sample?id=3"
        }
    ]
    
    # Pagination info
    context.total_items = len(context.data)
    context.start_item = 1
    context.end_item = context.total_items
    context.has_prev = False
    context.has_next = False
    
    # Primary key for row selection
    context.primary_key = "id"
