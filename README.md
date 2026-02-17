# Django + Datastar Examples

A comprehensive collection of examples demonstrating how to build hypermedia-driven web applications using [Datastar](https://data-star.dev/) with Django.

## What is Datastar?

Datastar is a hypermedia framework that combines the best of [HTMX](https://htmx.org/) (server-side rendering) and [Alpine.js](https://alpinejs.dev/) (client-side reactivity). It enables you to build modern, reactive web applications using a hypermedia approach where the server sends HTML fragments that Datastar merges into the DOM.

Key features:

- **Server-Sent Events (SSE)** for real-time updates
- **Signals** for client-side state management
- **Fragment merging** using idiomorph

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

## Examples

This project includes 12 practical examples, each demonstrating a common Datastar pattern:

| # | Example | Description |
|---|---------|-------------|
| 01 | [Active Search]({% url 'examples:active-search' %}) | Search contacts with debounced input |
| 02 | [Click to Load]({% url 'examples:click-to-load' %}) | Pagination with "Load More" button |
| 03 | [Edit Row]({% url 'examples:edit-row' %}) | Inline editing for table rows |
| 04 | [Delete Row]({% url 'examples:delete-row' %}) | Remove rows with animation |
| 05 | [TodoMVC]({% url 'examples:todo-mvc' %}) | Classic todo app implementation |
| 06 | [Inline Validation]({% url 'examples:inline-validation' %}) | Real-time form validation |
| 07 | [Infinite Scroll]({% url 'examples:infinite-scroll' %}) | Auto-load more on scroll |
| 08 | [Lazy Tabs]({% url 'examples:lazy-tabs' %}) | Load tab content on demand |
| 09 | [File Upload]({% url 'examples:file-upload' %}) | Upload with progress indicator |
| 10 | [Sortable]({% url 'examples:sortable' %}) | Drag-and-drop reordering |
| 11 | [Notifications]({% url 'examples:notifications' %}) | Real-time notification counter |
| 12 | [Bulk Update]({% url 'examples:bulk-update' %}) | Select and update multiple items |

## Project Structure

```
django-datastar-examples/
├── config/
│   ├── settings.py      # Django settings
│   └── urls.py          # Root URL configuration
├── examples/
│   ├── models.py        # Example models (Contact, Todo, Notification, Item)
│   ├── views.py         # View handlers for all examples
│   ├── urls.py          # Example URLs (kebab-case)
│   └── templates/
│       └── examples/
│           ├── index.html           # Main examples index
│           └── *.html              # 12 example templates
├── docs/
│   └── datastar-guide/             # Comprehensive Datastar guide
├── templates/
│   └── base.html        # Base template with Datastar script
└── manage.py
```

## Documentation

Detailed documentation is available in the `docs/datastar-guide/` directory:

- [Introduction](docs/datastar-guide/introduction.md) - What is Datastar?
- [Installation](docs/datastar-guide/installation.md) - Setup guide
- [Core Concepts](docs/datastar-guide/core-concepts.md) - Signals, SSE, fragments
- [Django Integration](docs/datastar-guide/django-integration.md) - Using datastar-py
- [Attributes Reference](docs/datastar-guide/datastar-attributes-reference.md) - Complete attribute reference
- [Actions Reference](docs/datastar-guide/datastar-actions-reference.md) - Actions like @get, @post
- [Common Patterns](docs/datastar-guide/common-patterns.md) - Ready-to-use patterns
- [Best Practices](docs/datastar-guide/best-practices.md) - Recommended patterns
- [Troubleshooting](docs/datastar-guide/troubleshooting.md) - Common issues and solutions

## Adding a New Example

1. **Create a model** (if needed) in `examples/models.py`

2. **Add views** in `examples/views.py`:
   - Main view: renders the page with initial state
   - AJAX endpoint: returns Datastar SSE response using `DjangoDatastar`

3. **Create template** in `examples/templates/examples/`

4. **Add URLs** in `examples/urls.py` using kebab-case

5. **Update index** in `examples/templates/examples/index.html`

6. **Run formatters:**

   ```bash
   ruff format .
   djade .
   ```

## Models

The project includes four models for demonstrations:

- **Contact** - For search and CRUD examples
- **Todo** - For TodoMVC example
- **Notification** - For notifications example
- **Item** - For sortable example

## Resources

- [Datastar Documentation](https://data-star.dev/)
- [datastar-py SDK](https://pypi.org/project/datastar-py/)
- [Datastar GitHub](https://github.com/starfederation/datastar)

## License

MIT
