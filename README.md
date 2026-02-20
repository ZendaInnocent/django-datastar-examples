# Django + Datastar Examples

[![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0+-green?logo=django)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Datastar](https://img.shields.io/badge/Datastar-0.8+-orange)](https://data-star.dev/)

A comprehensive collection of examples demonstrating how to build hypermedia-driven web applications using [Datastar](https://data-star.dev/) with Django.

## Table of Contents

- [What is Datastar?](#what-is-datastar)
- [Why Datastar?](#why-datastar)
- [Examples](#examples)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Models](#models)
- [Resources](#resources)
- [License](#license)

## What is Datastar?

Datastar is a hypermedia framework that combines the best of [HTMX](https://htmx.org/) (server-side rendering) and [Alpine.js](https://alpinejs.dev/) (client-side reactivity). It enables you to build modern, reactive web applications using a hypermedia approach where the server sends HTML fragments that Datastar merges into the DOM.

Key features:

- **Server-Sent Events (SSE)** for real-time updates
- **Signals** for client-side state management
- **Fragment merging** using idiomorph

## Why Datastar?

Datastar offers a compelling alternative to traditional SPA frameworks:

- **No JavaScript Required** - Build reactive UIs with pure HTML attributes
- **Progressive Enhancement** - Works without JavaScript, enhanced with it
- **Small Bundle Size** - ~15KB vs hundreds of KB for React/Vue/Angular
- **Django-Native** - Use Server-Sent Events (SSE) for real-time updates
- **Simple Mental Model** - Server sends HTML or signals, browser merges it - no virtual DOM

```python
# A Datastar view in Django - that's all it takes
from datastar_py.django import datastar_response, read_signals, ServerSentGenerator as SSE

@datastar_response
def search_view(request):
   signals = read_signals(request)
    query = signals.get('query')
    contacts = Contact.objects.filter(name__icontains=query)

    html = render_to_string('fragments/contact_list.html', {'contacts': contacts})
    yield SSE.patch_elements(html, selector='#results')
```

## Examples

This project includes 13 practical examples, each demonstrating a common Datastar pattern:

| #   | Example          | Description                                |
| --- | ---------------- | ------------------------------------------ |
| 1   | Active Search    | Real-time search with debounced queries    |
| 2   | Click to Load    | Load more content on button click         |
| 3   | Edit Row         | Inline row editing with instant updates   |
| 4   | File Upload      | Progress tracking for file uploads via SSE |
| 5   | Infinite Scroll  | Auto-load content as user scrolls         |
| 6   | Lazy Tabs        | Tab content loaded on first activation    |
| 7   | Merge Tags       | Fragment merging with ID matching         |
| 8   | Modal            | Dynamic modal dialogs                     |
| 9   | Notifications    | Real-time toast notifications             |
| 10  | Sortable         | Drag-and-drop reordering                  |
| 11  | TodoMVC          | Full CRUD Todo application                |
| 12  | Validation       | Form validation with error feedback       |
| 13  | System Messages  | User feedback messages (success, error, info) |

### Home Page

| Light Mode                                | Dark Mode                               |
| ----------------------------------------- | --------------------------------------- |
| ![Home Light](screenshots/home-light.png) | ![Home Dark](screenshots/home-dark.png) |

### Screenshots

| Example       | Light Mode                                            | Dark Mode                                            |
| ------------- | ----------------------------------------------------- | ---------------------------------------------------- |
| Active Search | ![Active Search](screenshots/active-search-light.png) | ![Active Search](screenshots/active-search-dark.png) |
| Click to Load | ![Click to Load](screenshots/clicktoload-light.png)   | ![Click to Load](screenshots/clicktoload-dark.png)   |
| Edit Row      | ![Edit Row](screenshots/editrow-light.png)            | ![Edit Row](screenshots/editrow-dark.png)            |
| File Upload   | ![File Upload](screenshots/fileupload-light.png)      | ![File Upload](screenshots/fileupload-dark.png)      |
| Lazy Tabs     | ![Lazy Tabs](screenshots/lazytabs-light.png)          | ![Lazy Tabs](screenshots/lazytabs-dark.png)          |
| Sortable      | ![Sortable](screenshots/sortable-light.png)           | ![Sortable](screenshots/sortable-dark.png)           |
| Notifications | ![Notifications](screenshots/notifications-light.png) | ![Notifications](screenshots/notifications-dark.png) |

## Quick Start

1. **Clone the repository**

2. **Create and activate virtual environment**

   ```bash
   uv venv
   uv sync
   ```

3. **Copy environment variables**

   ```bash
   cp .env_sample .env
   ```

4. **Run migrations**

   ```bash
   uv run python manage.py migrate
   ```

5. **Seed sample data** (optional)

   ```bash
   uv run python manage.py seed_data
   ```

6. **Start the development server**

   ```bash
   uv run python manage.py runserver
   ```

7. **Visit** http://127.0.0.1:8000/

## Project Structure

```
django-datastar-examples/
├── config/                  # Django settings and configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── examples/                # Main application with examples
│   ├── models.py            # Demo models (Contact, Todo, etc.)
│   ├── views.py             # View handlers
│   ├── urls.py              # URL routing
│   └── templates/examples/  # Example templates
├── templates/               # Base templates
├── docs/                   # Documentation
│   └── datastar-guide/     # Datastar integration guide
├── pyproject.toml           # Project dependencies
└── manage.py                # Django management script
```

## Models

The project includes four models for demonstrations:

- **Contact** - For search and CRUD examples
- **Todo** - For TodoMVC example
- **Notification** - For notifications example
- **Item** - For sortable example

## Resources

- [Datastar Documentation](https://data-star.dev/)
- [Datastar Python SDK](https://github.com/starfederation/datastar-python/)

## License

MIT
