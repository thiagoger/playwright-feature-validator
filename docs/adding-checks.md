# Adding Health Checks

This guide explains how to create custom health checks.

## Check Structure

Each check is defined in JSON with this structure:

```json
{
  "id": "unique-check-id",
  "name": "Human Readable Name",
  "type": "navigation",
  "priority": "high",
  "route": "/app/page",
  "expect": {
    "selector": ".element-to-find"
  },
  "highlight": {
    "type": "box",
    "selector": ".element-to-highlight"
  }
}
```

## Check Types

### 1. Auth Check

Validates login works.

```json
{
  "id": "login-works",
  "name": "Login Works",
  "type": "auth",
  "priority": "critical",
  "expect": {
    "url_contains": "/app/"
  }
}
```

### 2. Navigation Check

Navigates to a page and validates elements.

```json
{
  "id": "customers-page",
  "name": "Customers Page Loads",
  "type": "navigation",
  "priority": "high",
  "route": "/app/customers",
  "expect": {
    "selector": ".customer-list",
    "min_count": 1
  }
}
```

### 3. UI Check

Validates UI elements exist.

```json
{
  "id": "menu-visible",
  "name": "Menu is Visible",
  "type": "ui",
  "priority": "medium",
  "expect": {
    "selector": "nav.main-menu"
  }
}
```

### 4. API Check (Future)

Validates API endpoints.

```json
{
  "id": "api-health",
  "name": "API Health Check",
  "type": "api",
  "priority": "critical",
  "endpoint": "/api/health",
  "expect": {
    "status": 200
  }
}
```

## Expectations

### Selector Exists

```json
"expect": {
  "selector": ".my-element"
}
```

### Minimum Count

```json
"expect": {
  "selector": ".row",
  "min_count": 10
}
```

### URL Contains

```json
"expect": {
  "url_contains": "/dashboard"
}
```

### Text Contains

```json
"expect": {
  "selector": "h1",
  "text": "Welcome"
}
```

## Annotations

Add visual annotations to screenshots:

### Box Highlight

```json
"highlight": {
  "type": "box",
  "selector": ".important-element"
}
```

### Arrow Pointer

```json
"highlight": {
  "type": "arrow",
  "selector": ".button"
}
```

## Priority Levels

| Priority | When to Use |
|----------|-------------|
| critical | Login, core features |
| high | Important features |
| medium | Standard features |
| low | Nice-to-have checks |

## Example: Complete Check

```json
{
  "id": "create-invoice-works",
  "name": "Can Create Invoice",
  "type": "navigation",
  "priority": "high",
  "route": "/app/invoice/new",
  "timeout": 10000,
  "expect": {
    "selector": "form.invoice-form",
    "url_contains": "/invoice"
  },
  "highlight": {
    "type": "box",
    "selector": "form.invoice-form"
  }
}
```

## Adding to Product

1. Open `config/checks/{product}.json`
2. Add your check to the `checks` array
3. Run `feature-checker list --product {product}` to verify
4. Run the check: `feature-checker run --product {product} --check {id}`
