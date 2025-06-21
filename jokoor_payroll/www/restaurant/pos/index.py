import frappe
from frappe.utils import getdate, get_time, now

def get_context(context):
    if not frappe.session.user or frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect

    # Dummy categories
    context.categories = [
        {"name": "main", "category_name": "Main Course", "description": "Main dishes"},
        {"name": "appetizers", "category_name": "Appetizers", "description": "Starters"},
        {"name": "desserts", "category_name": "Desserts", "description": "Sweet treats"},
        {"name": "drinks", "category_name": "Beverages", "description": "Drinks"},
    ]

    # Dummy menu items
    context.menu_items = [
        {
            "name": "burger-1",
            "item_name": "Classic Burger",
            "category": "main",
            "price": 150.00,
            "description": "Juicy beef patty with fresh vegetables",
            "image": "https://placehold.co/300x200",
            "is_available": 1
        },
        {
            "name": "pizza-1",
            "item_name": "Margherita Pizza",
            "category": "main",
            "price": 200.00,
            "description": "Traditional Italian pizza with tomatoes and mozzarella",
            "image": "https://placehold.co/300x200",
            "is_available": 1
        },
        {
            "name": "salad-1",
            "item_name": "Caesar Salad",
            "category": "appetizers",
            "price": 80.00,
            "description": "Fresh romaine lettuce with Caesar dressing",
            "image": "https://placehold.co/300x200",
            "is_available": 1
        },
        {
            "name": "wings-1",
            "item_name": "Buffalo Wings",
            "category": "appetizers",
            "price": 120.00,
            "description": "Spicy chicken wings with blue cheese dip",
            "image": "https://placehold.co/300x200",
            "is_available": 1
        },
        {
            "name": "cake-1",
            "item_name": "Chocolate Cake",
            "category": "desserts",
            "price": 90.00,
            "description": "Rich chocolate cake with ganache",
            "image": "https://placehold.co/300x200",
            "is_available": 1
        },
        {
            "name": "ice-cream-1",
            "item_name": "Ice Cream Sundae",
            "category": "desserts",
            "price": 70.00,
            "description": "Vanilla ice cream with toppings",
            "image": "https://placehold.co/300x200",
            "is_available": 1
        },
        {
            "name": "soda-1",
            "item_name": "Soft Drink",
            "category": "drinks",
            "price": 30.00,
            "description": "Assorted sodas",
            "image": "https://placehold.co/300x200",
            "is_available": 1
        },
        {
            "name": "coffee-1",
            "item_name": "Coffee",
            "category": "drinks",
            "price": 40.00,
            "description": "Freshly brewed coffee",
            "image": "https://placehold.co/300x200",
            "is_available": 1
        }
    ]

    # Dummy tables
    context.tables = [
        {"name": "T1", "table_number": "1", "capacity": 2, "status": "Available"},
        {"name": "T2", "table_number": "2", "capacity": 4, "status": "Available"},
        {"name": "T3", "table_number": "3", "capacity": 4, "status": "Occupied"},
        {"name": "T4", "table_number": "4", "capacity": 6, "status": "Available"},
        {"name": "T5", "table_number": "5", "capacity": 8, "status": "Occupied"}
    ]

    # Dummy active orders
    context.active_orders = [
        {
            "name": "ORD001",
            "table": "Table 1",
            "customer_name": "John Doe",
            "order_status": "New",
            "total_amount": 380.00,
            "creation": "2025-04-29 10:30:00"
        },
        {
            "name": "ORD002",
            "table": "Table 3",
            "customer_name": "Jane Smith",
            "order_status": "In Progress",
            "total_amount": 450.00,
            "creation": "2025-04-29 10:15:00"
        },
        {
            "name": "ORD003",
            "table": "Table 5",
            "customer_name": "Bob Wilson",
            "order_status": "Ready",
            "total_amount": 270.00,
            "creation": "2025-04-29 10:00:00"
        }
    ]

    context.current_date = getdate(now())
    context.current_time = get_time(now()).strftime("%I:%M %p")
