# `button` Component Usage Guide

The `button` macro is a reusable component for rendering styled buttons in Frappe/Jinja templates. It supports different types, sizes, icons, and custom classes for flexible use in forms and UIs.

---

## 1. Import the Macro

At the top of your template:
```jinja
{% from "templates/components/button.html" import button %}
```

---

## 2. Basic Usage Example

```jinja
{{ button(text="Save", type="primary", btn_type="submit") }}
```

---

## 3. Parameters

- `text` (string, required): The button label.
- `type` (string, optional): Button style (`primary`, `secondary`, etc.).
- `btn_type` (string, optional): HTML button type (`button`, `submit`, `reset`).
- `size` (string, optional): Button size (`small`, `medium`, `large`).
- `icon` (string, optional): FontAwesome icon class (e.g., `save`).
- `classes` (string, optional): Extra CSS classes for the button.

---

## 4. Example Usages

```jinja
{{ button(text="Add", type="secondary", size="small", icon="plus") }}
{{ button(text="Delete", type="danger", btn_type="button", classes="ml-2") }}
```

---

## 5. Tips

- Use `btn_type="submit"` for form submission buttons.
- Use the `icon` parameter to add a FontAwesome icon before the text.
- Combine with custom classes for layout or color.

---

**Create beautiful, consistent buttons for your app!** 