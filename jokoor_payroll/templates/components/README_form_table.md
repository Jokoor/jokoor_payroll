# `form_table` Component Usage Guide

The `form_table` macro is a reusable, dynamic, and editable table component for Frappe/Jinja templates. It supports input, select (with Select2), and date (with daterangepicker) fields, and allows dynamic row addition/removal with full support for field properties like `readonly`, `disabled`, `required`, etc.

---

## 1. Import the Macro

At the top of your template:
```jinja
{% from "templates/components/form_table.html" import form_table %}
```

---

## 2. Basic Usage Example

```jinja
{{ form_table(
    id="items-table",
    columns=[
        {"id": "item", "label": "Item", "type": "input", "required": true},
        {"id": "qty", "label": "Qty", "type": "input", "input_type": "number", "min": 1, "step": 1},
        {"id": "rate", "label": "Rate", "type": "input", "input_type": "number", "readonly": true},
        {"id": "amount", "label": "Amount", "type": "input", "input_type": "number", "readonly": true, "disabled": true}
    ],
    rows=[
        {"item": "Apple", "qty": 2, "rate": 5, "amount": 10},
        {"item": "Banana", "qty": 3, "rate": 4, "amount": 12}
    ],
    add_button_text="Add Item"
) }}
```

---

## 3. Column Definition

Each column is a dictionary with these keys:
- `id`: Field name (string, required)
- `label`: Column header (string, required)
- `type`: Field type (`input`, `select`, `date`)
- `input_type`: For `input` fields, HTML input type (e.g. `text`, `number`)
- `options`: For `select` fields, a list of options (strings or `{value, label}` objects)
- `placeholder`: Placeholder text
- `readonly`, `disabled`, `required`: Boolean field properties
- `min`, `max`, `step`: For number/date fields

Example:
```jinja
{"id": "qty", "label": "Qty", "type": "input", "input_type": "number", "min": 1, "step": 1}
```

---

## 4. Supported Field Types

- `input`: Standard input field (supports all HTML input types)
- `select`: Dropdown (uses Select2 for search)
- `date`: Date picker (uses daterangepicker)

---

## 5. Dynamic Row Addition

- The "Add Row" button adds a new row with all field properties applied.
- The "Remove" button deletes a row.
- All plugins (Select2, daterangepicker) are initialized for new rows automatically.

---

## 6. Field Properties

You can pass any of these properties in your column definition:
- `readonly`: Makes the field read-only
- `disabled`: Disables the field
- `required`: Makes the field required
- `min`, `max`, `step`: For number/date fields

Example:
```jinja
{"id": "rate", "label": "Rate", "type": "input", "input_type": "number", "readonly": true}
```

---

## 7. Calculations & Custom Logic

You can use jQuery in your page to access and process table data. For example, to calculate `amount = qty * rate`:

```js
function updateAmounts(tableId) {
  $('#' + tableId + ' tbody tr').each(function() {
    var $row = $(this);
    var qty = parseFloat($row.find('input[name^="qty"]').val()) || 0;
    var rate = parseFloat($row.find('input[name^="rate"]').val()) || 0;
    var amount = qty * rate;
    $row.find('input[name^="amount"]').val(amount ? amount.toFixed(2) : '');
  });
}

$(document).ready(function() {
  $('#items-table').on('input', 'input[name^="qty"], input[name^="rate"]', function() {
    updateAmounts('items-table');
  });
  updateAmounts('items-table');
});
```

---

## 8. Plugin Integration

- **Select2**: All select fields use Select2 for search and clear.
- **Daterangepicker**: All date fields use daterangepicker for date selection.
- All required JS/CSS is included in the macro, but ensure you do not include jQuery, Select2, or daterangepicker multiple times in your project.

---

## 9. Tips

- Always use unique `id` for each table instance.
- You can use any valid HTML input property in your column definition.
- For advanced use, you can extend the macro to support more field types or custom rendering.

---

## 10. Example: Minimal Table

```jinja
{{ form_table(
    id="simple-table",
    columns=[
        {"id": "name", "label": "Name", "type": "input"},
        {"id": "role", "label": "Role", "type": "select", "options": ["Admin", "User"]}
    ],
    rows=[
        {"name": "Alice", "role": "Admin"}
    ],
    add_button_text="Add Row"
) }}
```

---

## 11. Troubleshooting

- If dynamic rows do not get plugin features, check that your page does not include jQuery, Select2, or daterangepicker more than once.
- If you get a Jinja error, ensure you are not using Jinja `{% if ... %}` inside JavaScript blocks.

---

**Enjoy building dynamic, editable tables!** 