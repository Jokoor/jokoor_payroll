import frappe

def get_context(context):
    context.form_id = "new-inventory-item"
    context.form_action = "/api/inventory/create/create/create"
    context.form_method = "POST"
    context.show_submit_button = True
    context.submit_button_text = "Create Item"
    context.form_validate = True
    context.active_page = "inventory"
    
    # Define form sections and fields
    context.form_sections = [
        {
            "title": "Basic Information",
            "icon": "fa-info-circle",
            "description": "Enter the basic details of the inventory item",
            "width": 6,
            "fields": [
                {
                    "type": "text",
                    "name": "item_code",
                    "label": "Item Code",
                    "required": True,
                    "placeholder": "e.g., JKR-001",
                    "help": "Unique identifier for the item",
                    "width": 6
                },
                {
                    "type": "text",
                    "name": "name",
                    "label": "Item Name",
                    "required": True,
                    "placeholder": "e.g., Basmati Rice",
                    "width": 6
                },
                {
                    "type": "select",
                    "name": "category",
                    "label": "Category",
                    "required": True,
                    "width": 6,
                    "options": [
                        {"value": "grains", "label": "Grains"},
                        {"value": "meat", "label": "Meat"},
                        {"value": "vegetables", "label": "Vegetables"},
                        {"value": "dairy", "label": "Dairy"},
                        {"value": "spices", "label": "Spices"},
                        {"value": "oils", "label": "Oils"},
                        {"value": "baking", "label": "Baking"},
                        {"value": "herbs", "label": "Herbs"}
                    ]
                },
                {
                    "type": "select",
                    "name": "unit",
                    "label": "Unit",
                    "required": True,
                    "width": 6,
                    "options": [
                        {"value": "kg", "label": "Kilogram (kg)"},
                        {"value": "g", "label": "Gram (g)"},
                        {"value": "l", "label": "Liter (L)"},
                        {"value": "ml", "label": "Milliliter (ml)"},
                        {"value": "pcs", "label": "Pieces"},
                        {"value": "box", "label": "Box"}
                    ]
                }
            ]
        },
        {
            "title": "Stock Information",
            "icon": "fa-box",
            "description": "Set the stock levels and pricing",
            "width": 6,
            "fields": [
                {
                    "type": "number",
                    "name": "quantity",
                    "label": "Initial Quantity",
                    "required": True,
                    "placeholder": "0",
                    "width": 6
                },
                {
                    "type": "number",
                    "name": "reorder_level",
                    "label": "Reorder Level",
                    "required": True,
                    "placeholder": "10",
                    "help": "Minimum quantity before reordering",
                    "width": 6
                },
                {
                    "type": "currency",
                    "name": "unit_price",
                    "label": "Unit Price",
                    "required": True,
                    "placeholder": "0.00",
                    "prefix": "GMD",
                    "width": 6
                },
                {
                    "type": "currency",
                    "name": "total_value",
                    "label": "Total Value",
                    "readonly": True,
                    "prefix": "GMD",
                    "width": 6
                }
            ]
        },
        {
            "title": "Additional Information",
            "icon": "fa-clipboard",
            "description": "Optional details about the item",
            "width": 12,
            "fields": [
                {
                    "type": "textarea",
                    "name": "description",
                    "label": "Description",
                    "placeholder": "Enter item description...",
                    "width": 12,
                    "rows": 4
                },
                {
                    "type": "text",
                    "name": "supplier",
                    "label": "Supplier",
                    "placeholder": "Enter supplier name",
                    "width": 6
                },
                {
                    "type": "text",
                    "name": "location",
                    "label": "Storage Location",
                    "placeholder": "e.g., Kitchen Storage A1",
                    "width": 6
                }
            ]
        }
    ]