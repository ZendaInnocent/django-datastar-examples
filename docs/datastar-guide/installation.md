# Installation

## Step 1: Install datastar-py

```bash
# Using uv (recommended for this project)
cd src && uv add datastar-py

# Or using pip
pip install datastar-py
```

## Step 2: Add to Django Settings

```python
# settings.py
INSTALLED_APPS = [
    # ... your existing apps
]
```

No app registration needed - `datastar-py` is a pure SDK library.

## Step 3: Include Datastar CDN

Add to your base template:

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}Dashboard{% endblock %}</title>
    {% load static %}
    <link
      rel="stylesheet"
      href="{% static 'css/styles.css' %}" />
  </head>
  <body>
    {% block content %}{% endblock %}

    <!-- DATSTAR REQUIRED -->
    <script
      type="module"
      src="https://cdn.jsdelivr.net/gh/starfederation/datastar@v1.0.0-RC.7/bundles/datastar.js"></script>
  </body>
</html>
```

---
