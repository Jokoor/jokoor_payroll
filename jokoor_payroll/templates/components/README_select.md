# `select` Component Usage Guide

The `select` macro is a reusable component for rendering styled dropdown fields in Frappe/Jinja templates. It supports Select2 for search, custom options, and flexible styling.

---

## 1. Import the Macro

At the top of your template:
```jinja
{% from "templates/components/select.html" import select %}
```

---

## 2. Basic Usage Example

```jinja
{{ select(id="gender", label="Gender", options=[{"value": "M", "label": "Male"}, {"value": "F", "label": "Female"}], placeholder="Select gender") }}
```

---

## 3. Parameters

- `id` (string, required): The select's id and name.
- `label` (string, required): The label for the select.
- `options` (list, required): List of options (strings or `{value, label}` objects).
- `placeholder` (string, optional): Placeholder text.
- `search` (bool, optional): Enable search (default: true).
- `show_label` (bool, optional): Show the label (default: true).
- `width` (int, optional): Column width (1-12, optional).
- `size` (string, optional): `small`, `medium`, or `large` (default: `large`).
- `classes` (string, optional): Extra CSS classes for the wrapper.

---

## 4. Example Usages

```jinja
{{ select(id="country", label="Country", options=["USA", "Canada", "UK"], size="small") }}
{{ select(id="role", label="Role", options=[{"value": "admin", "label": "Admin"}, {"value": "user", "label": "User"}], search=false) }}
```

---

## 5. Tips

- Use `search=false` to disable the search box.
- Use `size` to match the select to your input field sizes.
- Options can be simple strings or objects with `value` and `label`.
- Select2 is used for enhanced dropdowns and search.

---

**Create beautiful, searchable dropdowns with ease!** 