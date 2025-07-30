# Jokoor Card Component

A flexible and responsive card component that follows the Carbon Design System. The component supports both stat cards and regular content cards with various customization options.

## Usage

### Basic Setup

1. Include the card component in your template:
```html
{% include "templates/includes/components/card.html" %}
```

2. Create a grid container for your cards:
```html
<div class="jk-cards-grid">
    <!-- Your cards will go here -->
</div>
```

### Card Types

#### 1. Stat Card
Used for displaying statistics with an icon and trend indicator.

```html
{% set card_type = 'stat' %}
{% set title = 'Total Users' %}
{% set count = '2,547' %}
{% set icon = 'fa-users' %}
{% set color = 'primary' %}
{% set width = 3 %}
{% set footer = '<i class="fas fa-arrow-up jk-trend-up"></i> <span class="jk-trend-up">12%</span> vs last month' %}
{% include "templates/includes/components/card.html" %}
```

#### 2. Regular Card
Used for general content, with optional header, subtitle, and actions.

```html
{% set card_type = 'default' %}
{% set title = 'Card Title' %}
{% set subtitle = 'Optional subtitle' %}
{% set content = 'Your content here' %}
{% set actions = '<button class="jk-card-action-btn primary">Action</button>' %}
{% set width = 4 %}
{% include "templates/includes/components/card.html" %}
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| card_type | string | 'default' | Type of card ('stat' or 'default') |
| title | string | - | Card title |
| subtitle | string | - | Subtitle (only for default cards) |
| content | string | - | Main content (HTML supported) |
| count | string | - | Number/value (only for stat cards) |
| icon | string | - | FontAwesome icon class (only for stat cards) |
| color | string | - | Card color theme ('primary', 'success', 'info', 'warning', 'danger') |
| width | number | 3 | Card width (1-12, follows 12-column grid) |
| actions | string | - | Action buttons HTML (only for default cards) |
| footer | string | - | Footer content (HTML supported) |
| classes | string | - | Additional CSS classes |

### Grid System

The card component uses a responsive 12-column grid system:

- **Mobile (320px+)**: Cards stack full width
- **Tablet (672px+)**: 
  - width-1 = 3 columns (25%)
  - width-2 = 6 columns (50%)
  - width-3 = 9 columns (75%)
  - width-4 = 12 columns (100%)
- **Small Desktop (1056px+)**:
  - width-1 = 2 columns (16.67%)
  - width-2 = 4 columns (33.33%)
  - width-3 = 6 columns (50%)
  - width-4 = 8 columns (66.67%)
  - width-5 = 10 columns (83.33%)
  - width-6 = 12 columns (100%)
- **Large Desktop (1312px+)**:
  - Supports all widths from 1-12 columns

### Color Variants

Available color variants for cards:
- `primary` - Purple theme (#5534c9)
- `success` - Green theme
- `info` - Blue theme
- `warning` - Yellow theme
- `danger` - Red theme

### Example Usage

```html
<h2 class="jk-section-title">Dashboard Cards</h2>
<div class="jk-cards-grid">
    <!-- Stat Card -->
    {% set card_type = 'stat' %}
    {% set title = 'Total Sales' %}
    {% set count = '$45,678' %}
    {% set icon = 'fa-dollar-sign' %}
    {% set color = 'primary' %}
    {% set width = 3 %}
    {% set footer = '<i class="fas fa-arrow-up jk-trend-up"></i> <span class="jk-trend-up">8%</span> vs last month' %}
    {% include "templates/includes/components/card.html" %}

    <!-- Regular Card -->
    {% set card_type = 'default' %}
    {% set title = 'Recent Activity' %}
    {% set subtitle = 'Last 7 days' %}
    {% set content %}
        <div style="display: flex; flex-direction: column; gap: 1rem;">
            <!-- Your content here -->
        </div>
    {% endset %}
    {% set actions = '<button class="jk-card-action-btn primary">View All</button>' %}
    {% set width = 6 %}
    {% include "templates/includes/components/card.html" %}
</div>
```

### CSS Classes

The component provides several utility classes:
- `jk-cards-grid` - Container for cards
- `jk-section-title` - Section headings
- `jk-trend-up` - Green trend indicator
- `jk-trend-down` - Red trend indicator
- `jk-card-action-btn` - Button styles (use with `primary` or `secondary`)

### Best Practices

1. Always wrap cards in a `jk-cards-grid` container
2. Use appropriate width values based on content importance and layout needs
3. Keep stat card content concise and focused
4. Use consistent color variants for similar types of information
5. Consider mobile responsiveness when setting card widths
