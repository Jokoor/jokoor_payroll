# `input` Component Usage Guide

The `input` macro is a reusable component for rendering styled input fields in Frappe/Jinja templates. It supports various input types, validation, and custom classes.

---

## 1. Import the Macro

At the top of your template:
```jinja
{% from "templates/components/input.html" import input %}
```

---

## 2. Basic Usage Example

```jinja
{{ input(id="email", label="Email", value="", type="email", required=true) }}
```

---

## 3. Parameters

- `id` (string, required): The input's id and name.
- `label` (string, required): The label for the input.
- `value` (string, optional): The input's value.
- `type` (string, optional): HTML input type (default: `text`).
- `placeholder` (string, optional): Placeholder text.
- `required` (bool, optional): Whether the field is required.
- `error` (string, optional): Error message to display.
- `info` (string, optional): Info/help text to display.
- `size` (string, optional): `small`, `medium`, or `large` (default: `large`).
- `classes` (string, optional): Extra CSS classes for the wrapper.

---

## 4. Example Usages

```jinja
{{ input(id="first_name", label="First Name", value="Alice") }}
{{ input(id="age", label="Age", type="number", size="small") }}
{{ input(id="password", label="Password", type="password", required=true, error="Password is required") }}
```

---

## 5. Tips

- Use the `error` parameter to show validation errors.
- Use the `info` parameter for help or hints.
- Combine with custom classes for layout or color.

---

**Build beautiful, accessible forms with ease!** 