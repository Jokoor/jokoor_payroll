# `date` Component Usage Guide

The `date` macro is a reusable component for rendering styled date picker fields in Frappe/Jinja templates. It uses the daterangepicker plugin for single date selection and supports custom classes and validation.

---

## 1. Import the Macro

At the top of your template:
```jinja
{% from "templates/components/date.html" import date %}
```

---

## 2. Basic Usage Example

```jinja
{{ date(id="dob", label="Date of Birth", value="01/01/2000") }}
```

---

## 3. Parameters

- `id` (string, required): The input's id and name.
- `label` (string, required): The label for the date field.
- `value` (string, optional): The date value (format: MM/DD/YYYY).
- `placeholder` (string, optional): Placeholder text.
- `required` (bool, optional): Whether the field is required.
- `error` (string, optional): Error message to display.
- `info` (string, optional): Info/help text to display.
- `size` (string, optional): `small`, `medium`, or `large` (default: `large`).
- `classes` (string, optional): Extra CSS classes for the wrapper.

---

## 4. Example Usages

```jinja
{{ date(id="start_date", label="Start Date", required=true) }}
{{ date(id="end_date", label="End Date", value="12/31/2024", size="small") }}
```

---

## 5. Tips

- The field uses the daterangepicker plugin for a modern date picker experience.
- Use the `error` parameter to show validation errors.
- Use the `info` parameter for help or hints.
- Combine with custom classes for layout or color.

---

**Add beautiful, interactive date pickers to your forms!** 