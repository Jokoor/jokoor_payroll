import frappe
from datetime import datetime, timedelta

def get_context(context):
    context.form_id = "view-inventory-item"
    context.form_editable = False
    context.form_locked = False
    context.show_submit_button = False
    
    # Dummy data for a single inventory item
    item_data = {
        "item_code": "JKR-001",
        "name": "Basmati Rice",
        "category": "grains",
        "unit": "kg",
        "quantity": 85,
        "reorder_level": 50,
        "unit_price": 75.00,
        "total_value": 6375.00,
        "description": "Premium quality Basmati rice imported from India. Long grain, aromatic rice perfect for biryanis and special rice dishes.",
        "supplier": "Global Foods Ltd",
        "location": "Kitchen Storage A1",
        "last_updated": "2025-04-28",
        "status": "In Stock"
    }
    
    # Transaction history
    context.transactions = [
        {
            "date": "2025-04-28",
            "type": "Purchase",
            "quantity": 100,
            "unit_price": 75.00,
            "total": 7500.00,
            "reference": "PO-2025-042"
        },
        {
            "date": "2025-04-28",
            "type": "Usage",
            "quantity": -15,
            "unit_price": 75.00,
            "total": -1125.00,
            "reference": "KIT-2025-089"
        }
    ]
    
    # Define form sections and fields
    context.form_sections = [
        {
            "title": "Basic Information",
            "icon": "fa-info-circle",
            "description": "Basic details of the inventory item",
            "width": 6,
            "fields": [
                {
                    "type": "text",
                    "name": "item_code",
                    "label": "Item Code",
                    "value": item_data["item_code"],
                    "readonly": True,
                    "width": 6
                },
                {
                    "type": "text",
                    "name": "name",
                    "label": "Item Name",
                    "value": item_data["name"],
                    "width": 6
                },
                {
                    "type": "select",
                    "name": "category",
                    "label": "Category",
                    "value": item_data["category"],
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
                    "value": item_data["unit"],
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
            "description": "Current stock levels and pricing",
            "width": 6,
            "fields": [
                {
                    "type": "number",
                    "name": "quantity",
                    "label": "Current Quantity",
                    "value": item_data["quantity"],
                    "width": 6
                },
                {
                    "type": "number",
                    "name": "reorder_level",
                    "label": "Reorder Level",
                    "value": item_data["reorder_level"],
                    "width": 6
                },
                {
                    "type": "currency",
                    "name": "unit_price",
                    "label": "Unit Price",
                    "value": item_data["unit_price"],
                    "prefix": "GMD",
                    "width": 6
                },
                {
                    "type": "currency",
                    "name": "total_value",
                    "label": "Total Value",
                    "value": item_data["total_value"],
                    "prefix": "GMD",
                    "readonly": True,
                    "width": 6
                }
            ]
        },
        {
            "title": "Additional Information",
            "icon": "fa-clipboard",
            "description": "Additional details about the item",
            "width": 12,
            "fields": [
                {
                    "type": "textarea",
                    "name": "description",
                    "label": "Description",
                    "value": item_data["description"],
                    "width": 12,
                    "rows": 4
                },
                {
                    "type": "text",
                    "name": "supplier",
                    "label": "Supplier",
                    "value": item_data["supplier"],
                    "width": 6
                },
                {
                    "type": "text",
                    "name": "location",
                    "label": "Storage Location",
                    "value": item_data["location"],
                    "width": 6
                }
            ]
        }
    ]