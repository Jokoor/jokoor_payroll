# `card` Component Usage Guide

The `card` macro is a reusable component for displaying metrics, stats, or any content block in a card layout. It is designed for use in Frappe/Jinja templates and supports customization via parameters.

---

## 1. Import the Macro

At the top of your template:
```jinja
{% from "templates/components/card.html" import card %}
```

---

## 2. Basic Usage Example

```jinja
{{ card("Total Revenue", "$23,231") }}
```

---

## 3. Parameters

- `title` (string, required): The card's heading or label.
- `value` (string, required): The main value or content to display.
- `classes` (string, optional): Extra CSS classes for the card container (e.g., for grid or color styling).
- `value_classes` (string, optional): Extra CSS classes for the value/content (e.g., for color or emphasis).

---

## 4. Example Usages

```jinja
{{ card("Total Revenue", "$23,231") }}
{{ card("Active Users", "1,234", classes="col-4", value_classes="jk-text-primary") }}
{{ card("Conversion Rate", "12.5%", classes="col-3", value_classes="text-green-600 font-bold") }}
```

---

## 5. Customization Tips

- You can use the `classes` parameter to control the card's width, color, or layout in your grid system.
- Use the `value_classes` parameter to highlight or style the value (e.g., color for positive/negative trends).
- The macro can be used for any content block, not just metrics—simply pass the desired title and value.

---

## 6. Example in a Grid

```jinja
<div class="jk-row">
  {{ card("Total Revenue", "$23,231", classes="col-4") }}
  {{ card("Active Users", "1,234", classes="col-4") }}
  {{ card("Conversion Rate", "12.5%", classes="col-4") }}
</div>
```

---

**Enjoy building beautiful dashboards and metric cards!** 