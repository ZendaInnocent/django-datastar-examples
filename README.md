# Django + Datastar Examples

A collection of examples demonstrating how to use [Datastar](https://data-star.dev/) with Django for building hypermedia-driven web applications.

## What is Datastar?

Datastar is a hypermedia framework that combines the best of [HTMX](https://htmx.org/) (server-side rendering) and [Alpine.js](https://alpinejs.dev/) (client-side reactivity). It enables you to build modern, reactive web applications using a hypermedia approach where the server sends HTML fragments that Datastar merges into the DOM.

Key features:

- **Server-Sent Events (SSE)** for real-time updates
- **Signals** for client-side state management
- **Fragment merging** using idiomorph

## Prerequisites

- Python 3.10+
- Django 5.0+
- [uv](https://github.com/astral-sh/uv) (recommended)

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

5. **Start the development server**

   ```bash
   uv run python manage.py runserver
   ```

6. **Visit** http://127.0.0.1:8000/

## Examples

| Example                                                               | Description                                     |
| --------------------------------------------------------------------- | ----------------------------------------------- |
| [Active Search](https://data-star.dev/examples/active_search)         | Search a contacts database with debounced input |
| [Click to Load](https://data-star.dev/examples/click_to_load)         | Load more content on button click               |
| [Inline Validation](https://data-star.dev/examples/inline_validation) | Form validation without page reload             |
| [TodoMVC](https://data-star.dev/examples/todomvc)                     | Classic todo app implementation                 |

## Project Structure

```
django-datastar-examples/
├── config/
│   ├── settings.py      # Django settings
│   └── urls.py          # Root URL configuration
├── examples/
│   ├── models.py        # Example models
│   ├── views.py         # View handlers
│   ├── urls.py          # Example URLs
│   └── templates/
│       └── examples/
│           └── index.html
├── templates/
│   └── base.html        # Base template with Datastar script
└── manage.py
```

## Adding a New Example

1. **Create a model** (if needed) in `examples/models.py`

2. **Add views** in `examples/views.py`:
   - Main view: renders the page with initial state
   - AJAX endpoint: returns Datastar SSE response

3. **Create template** in `examples/templates/examples/`

4. **Add URLs** in `examples/urls.py`

5. **Update index** in `examples/templates/examples/index.html`

## Resources

- [Datastar Documentation](https://data-star.dev/)
- [datastar-py SDK](https://pypi.org/project/datastar-py/)

## License

MIT
