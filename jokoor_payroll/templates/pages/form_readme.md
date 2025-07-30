# Form Template Documentation

This document explains how to use the generic form template (`form.html`) for creating forms in your application.

## Basic Usage

To use the form template, extend it in your template and pass the required context data:

```html
{% extends "templates/pages/restaurant/form.html" %}
{% block page_content %}
  {# Your additional content here if needed #}
{% endblock %}
```

## Required Context Variables

Pass these variables to the template context in your Python route:

### Form Configuration
```python
context.update({
    "submit_url": "/your/submit/endpoint",  # Form submission URL
    "cancel_url": "/your/cancel/url",       # Cancel button redirect URL
    "form_title": "Your Form Title",        # Title shown at the top
    "form_description": "Description text"   # Optional form description
})
```

### Form Fields
```python
context.fields = [
    {
        "type": "section_break",
        "section_title": "Section Title",
        "section_description": "Optional description"
    },
    {
        "type": "text",              # Field type
        "name": "field_name",        # Field name/id
        "label": "Field Label",      # Display label
        "required": True,            # Is field required?
        "placeholder": "Enter...",   # Placeholder text
        "width": 4,                  # Column width (1-12)
        "value": "Default value"     # Pre-filled value
    }
]
```

### Action Buttons
```python
context.action_buttons = [
    {
        "label": "Button Label",
        "url": "/action/url",
        "action": "submit|print|navigate",  # Action type
        "class": "jk-btn-primary",         # Button style
        "icon": "fas fa-icon-name",        # FontAwesome icon
        "position": "left|right"           # Button position
    }
]
```

## Available Field Types

- `section_break`: Creates a new section with title
- `text`: Text input field
- `textarea`: Multiline text input
- `select`: Dropdown selection
- `checkbox`: Single checkbox
- `radio`: Radio button group
- `date`: Date picker
- `number`: Numeric input
- `email`: Email input
- `password`: Password input
- `file`: File upload

## Button Styles

Available button classes:
- `jk-btn-primary`: Blue (primary actions)
- `jk-btn-secondary`: Gray (secondary actions)
- `jk-btn-success`: Green (positive actions)
- `jk-btn-danger`: Red (destructive actions)
- `jk-btn-info`: Light blue (informative actions)
- `jk-btn-warning`: Orange (warning actions)

## Action Types

- `submit`: Validates form before submission
- `save`: Same as submit (with validation)
- `print`: Opens in new tab
- `navigate`: Simple page navigation

## Complete Example

```python
def get_context(context):
    context.update({
        "submit_url": "/restaurant/save",
        "cancel_url": "/restaurant/list",
        "form_title": "Restaurant Details",
        "form_description": "Enter restaurant information"
    })
    
    context.fields = [
        {
            "type": "section_break",
            "section_title": "Basic Information",
            "section_description": "General details"
        },
        {
            "type": "text",
            "name": "restaurant_name",
            "label": "Restaurant Name",
            "required": True,
            "placeholder": "Enter restaurant name",
            "width": 4
        }
    ]
    
    context.action_buttons = [
        {
            "label": "Print",
            "url": "/restaurant/print",
            "action": "print",
            "class": "jk-btn-secondary",
            "icon": "fas fa-print",
            "position": "left"
        },
        {
            "label": "Save & Send",
            "url": "/restaurant/save-and-send",
            "action": "submit",
            "class": "jk-btn-primary",
            "icon": "fas fa-paper-plane",
            "position": "right"
        }
    ]
```

## Best Practices

1. Always specify a `submit_url` and `cancel_url`
2. Group related fields under section breaks
3. Use appropriate field widths for responsive layout
4. Include clear labels and placeholders
5. Mark required fields appropriately
6. Use consistent button styling across forms
7. Position primary actions on the right
8. Include icons for better visual recognition

## Validation

- Required fields are automatically validated
- Custom validation can be added through JavaScript
- Error messages appear below invalid fields
- Fields are marked with red border when invalid
- Errors clear automatically when user starts typing

## Styling

The form includes built-in responsive styling:
- Mobile-friendly layout
- Consistent spacing
- Clear visual hierarchy
- Proper field alignment
- Responsive grid system
- Accessible color scheme
