import frappe

def get_context(context):
    # Get active tab from query params or default to "all_items"
    context.active_tab = frappe.form_dict.get("tab", "all_items")
    
    # Common page settings
    context.page_title = "Inventory Management"
    context.page_description = "View and manage inventory items"
    context.page_icon = "fa-box"
    context.has_sidebar = True
    context.active_page = "inventory"
    context.has_actions = True
    context.action_buttons = """
        <button class="btn btn-primary" onclick="window.location.href='/restaurant/inventory/new'">
            <i class="fas fa-plus me-2"></i>Add Item
        </button>
    """

    # Define breadcrumb 
    context.breadcrumb_items = [
        {"label": "Restaurant", "url": "/restaurant"},
        {"label": "Inventory", "url": "#"}
    ]

    # Get page parameters
    page_size = int(frappe.form_dict.get('page_size', 10))
    page = int(frappe.form_dict.get('page', 1))
    
    # Calculate start and end for pagination
    start = (page - 1) * page_size
    
    if context.active_tab == "all_items":
        context.show_new_button = True
        context.new_button_label = "Add Item"
        # All Items Table
        context.table_id = "all-items-table"
        context.total_count = 10
        context.current_page = page
        context.page_size = page_size
        context.columns = [
            {"key": "item_code", "label": "Item Code", "sortable": True},
            {"key": "name", "label": "Item Name", "sortable": True},
            {"key": "category", "label": "Category", "sortable": True},
            {"key": "quantity", "label": "Quantity", "sortable": True},
            {"key": "unit", "label": "Unit", "sortable": True},
            {"key": "unit_price", "label": "Unit Price", "sortable": True},
            {"key": "total_value", "label": "Total Value", "sortable": True},
            {"key": "status", "label": "Status", "sortable": True}
        ]
        context.data = [
            {
                "item_code": "JKR-001",
                "name": "Basmati Rice",
                "category": "Grains",
                "quantity": 85,
                "unit": "kg",
                "unit_price": "GMD 75.00",
                "total_value": "GMD 6,375.00",
                "status": "In Stock"
            },
            {
                "item_code": "JKR-002",
                "name": "Chicken Breast",
                "category": "Meat",
                "quantity": 25,
                "unit": "kg",
                "unit_price": "GMD 180.00",
                "total_value": "GMD 4,500.00",
                "status": "Low Stock"
            },
            {
                "item_code": "JKR-003",
                "name": "Olive Oil",
                "category": "Oils",
                "quantity": 45,
                "unit": "l",
                "unit_price": "GMD 250.00",
                "total_value": "GMD 11,250.00",
                "status": "In Stock"
            }
        ]
    elif context.active_tab == "item_groups":
        context.show_new_button = True
        context.new_button_label = "Add Item Group"
        # Item Groups Table
        context.table_id = "item-groups-table"
        context.total_count = 10
        context.current_page = page
        context.page_size = page_size
        context.columns = [
            {"key": "name", "label": "Group Name", "sortable": True},
            {"key": "items_count", "label": "Items", "sortable": True},
            {"key": "total_value", "label": "Total Value", "sortable": True},
            {"key": "description", "label": "Description", "sortable": False}
        ]
        context.data = [
            {
                "name": "Grains",
                "items_count": 8,
                "total_value": "GMD 15,250.00",
                "description": "Rice, wheat, and other grain products"
            },
            {
                "name": "Meat",
                "items_count": 12,
                "total_value": "GMD 28,500.00",
                "description": "Fresh and frozen meat products"
            },
            {
                "name": "Vegetables",
                "items_count": 15,
                "total_value": "GMD 8,750.00",
                "description": "Fresh vegetables and greens"
            },
            {
                "name": "Dairy",
                "items_count": 6,
                "total_value": "GMD 12,000.00",
                "description": "Milk, cheese, and dairy products"
            }
        ]
    else:
        context.show_new_button = True
        context.new_button_label = "Add Variant"
        # Variants Table
        context.table_id = "variants-table"
        context.total_count = 10
        context.current_page = page
        context.page_size = page_size
        context.columns = [
            {"key": "item_code", "label": "Item Code", "sortable": True},
            {"key": "name", "label": "Name", "sortable": True},
            {"key": "parent_item", "label": "Parent Item", "sortable": True},
            {"key": "attribute", "label": "Attribute", "sortable": True},
            {"key": "value", "label": "Value", "sortable": True},
            {"key": "quantity", "label": "Quantity", "sortable": True}
        ]
        context.data = [
            {
                "item_code": "JKR-001",
                "name": "Basmati Rice",
                "parent_item": "Rice",
                "attribute": "Type",
                "value": "Basmati",
                "quantity": 85
            },
            {
                "item_code": "JKR-004",
                "name": "Jasmine Rice",
                "parent_item": "Rice",
                "attribute": "Type",
                "value": "Jasmine",
                "quantity": 65
            },
            {
                "item_code": "JKR-002",
                "name": "Chicken Breast",
                "parent_item": "Chicken",
                "attribute": "Cut",
                "value": "Breast",
                "quantity": 25
            },
            {
                "item_code": "JKR-005",
                "name": "Chicken Thigh",
                "parent_item": "Chicken",
                "attribute": "Cut",
                "value": "Thigh",
                "quantity": 30
            }
        ]

    # Common table settings
    
    context.has_search = True
    context.search_placeholder = "Search items..."
    context.has_record_selector = True
    context.delete_action = True
    context.delete_url = "/api/inventory/delete"
    context.view_page = "/restaurant/inventory/view/:id"
    context.show_new_button = True
    context.new_button_label = "Add Item"
    context.show_export = True
    context.show_actions = True