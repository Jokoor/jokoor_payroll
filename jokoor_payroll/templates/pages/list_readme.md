# Restaurant List Page Template

This template provides a reusable list view with sorting, pagination, and row selection capabilities.

## Quick Start

1. Create your HTML file and extend the template:
```html
{% extends "templates/pages/restaurant_list.html" %}
```

2. Create your Python file with the same name and implement `get_context`:
```python
def get_context(context):
    # Required configurations
    context.title = "Your List Title"
    context.subtitle = "Optional subtitle description"
    context.add_new_url = "/your/create/url"
    
    # Define table columns
    context.columns = [
        {"key": "id", "label": "ID"},
        {"key": "name", "label": "Name"}
    ]
    
    # Add your data
    context.data = [
        {
            "id": 1,
            "name": "Item 1",
            "url": "/detail/1"  # Makes row clickable
        }
    ]
```

## Required Context Variables

| Variable | Type | Description |
|----------|------|-------------|
| `title` | string | Page title |
| `add_new_url` | string | URL for the "Add New" button |
| `columns` | array | Table column definitions |
| `data` | array | Table data |
| `primary_key` | string | Key field for row selection |

## Optional Context Variables

| Variable | Type | Description |
|----------|------|-------------|
| `subtitle` | string | Page subtitle |
| `total_items` | number | Total number of items |
| `start_item` | number | Start index for pagination |
| `end_item` | number | End index for pagination |
| `has_prev` | boolean | Whether previous page exists |
| `has_next` | boolean | Whether next page exists |

## Column Configuration

Each column object supports:
```python
{
    "key": "field_name",      # Data field to display
    "label": "Display Label", # Column header text
}
```

## Data Row Configuration

Each data row should be an object with:
- Fields matching the column keys
- Optional `url` field to make the row clickable
- Optional `status_html` field for formatted status badges

Example:
```python
{
    "id": 1,
    "name": "Example",
    "url": "/detail/1",
    "status_html": '<span class="badge badge-success">Active</span>'
}
```

## Status Badges

Pre-defined badge classes:
- `badge badge-success` - Green (Active/Success)
- `badge badge-warning` - Yellow (Pending/Warning)
- `badge badge-danger` - Red (Inactive/Error)

Example:
```python
row["status_html"] = '<span class="badge badge-success">Active</span>'
```

## Features

1. **Row Selection**
   - Checkbox in first column for row selection
   - "Select All" functionality
   - Selected count display

2. **Sorting**
   - Click column headers to sort
   - Automatic sort direction toggle

3. **Pagination**
   - Items per page selector (10, 25, 50, 100)
   - Page navigation controls
   - Item range display

4. **Clickable Rows**
   - Add `url` to data rows to make them clickable
   - Navigates to detail view on click

## Example Implementation

```python
def get_context(context):
    context.title = "Invoices"
    context.subtitle = "Manage your invoices"
    context.add_new_url = "/invoice/new"
    
    context.columns = [
        {"key": "invoice_number", "label": "Invoice Number"},
        {"key": "date", "label": "Date"},
        {"key": "customer", "label": "Customer"},
        {"key": "total", "label": "Total"},
        {"key": "status_html", "label": "Status"}
    ]
    
    context.data = [
        {
            "id": 1,
            "invoice_number": "INV-001",
            "date": "2025-04-30",
            "customer": "John Doe",
            "total": "$150.00",
            "status_html": '<span class="badge badge-success">Active</span>',
            "url": "/invoice/1"
        }
    ]
    
    context.primary_key = "id"
    context.total_items = len(context.data)
```
