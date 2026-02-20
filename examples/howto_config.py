"""
Advanced HowTo Configuration with Code Extraction

This module provides auto-generation of HowTo content by extracting
actual code from views, URLs, and templates.
"""

import inspect
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from django.urls import reverse

from examples import views


@dataclass
class HowToStep:
    """Represents a single step in the HowTo guide."""

    title: str
    description: str
    code: str
    language: str = 'python'  # python, html, django, javascript


@dataclass
class HowToExample:
    """Configuration for a single example's HowTo panel."""

    slug: str
    title: str
    description: str
    steps: list[HowToStep] = field(default_factory=list)
    doc_links: list[dict] = field(default_factory=list)

    # Internal - view functions
    _view_funcs: list[Callable] = field(default_factory=list, repr=False)
    _url_names: list[str] = field(default_factory=list, repr=False)
    _template_path: str = ''


def extract_view_code(view_func: Callable) -> str:
    """Extract the source code of a view function."""
    try:
        source = inspect.getsource(view_func)
        # Clean up the source
        lines = source.split('\n')
        # Remove first line (def ...)
        if lines:
            lines = lines[1:]
        # Remove indentation
        if lines:
            # Find minimum indentation
            min_indent = float('inf')
            for line in lines:
                if line.strip():
                    indent = len(line) - len(line.lstrip())
                    min_indent = min(min_indent, indent)

            # Remove common indentation
            cleaned = []
            for line in lines:
                if line.strip():
                    cleaned.append(
                        line[min_indent:] if min_indent < float('inf') else line
                    )
                else:
                    cleaned.append('')

            return '\n'.join(cleaned)
        return source
    except (TypeError, OSError):
        return '# Code not available'


def get_url_pattern(url_name: str) -> str:
    """Get the URL pattern for a named URL."""
    try:
        return reverse(f'examples:{url_name}')
    except Exception:
        return f'/{url_name}/'


def extract_template_code(template_path: str, max_lines: int = 20) -> str:
    """Extract code from a template file."""
    try:
        # Try multiple base paths
        base_paths = [
            Path('templates'),
            Path('examples/templates'),
        ]

        for base in base_paths:
            full_path = base / template_path
            if full_path.exists():
                with open(full_path, encoding='utf-8') as f:
                    lines = f.readlines()[:max_lines]
                return ''.join(lines)
    except Exception:
        pass
    return '# Template not available'


def build_active_search_steps() -> list[HowToStep]:
    """Build steps for Active Search example."""
    return [
        HowToStep(
            title='The View',
            description='Create a view that handles both regular page renders and Datastar requests. Use read_signals to read the search query:',
            code=extract_view_code(views.active_search_view),
            language='python',
        ),
        HowToStep(
            title='The URL',
            description='Add routes for the main view and search endpoint:',
            code="""path('active-search/', views.active_search_view, name='active-search'),
path('active-search/search/', views.active_search_search_view, name='active-search-search'),""",
            language='python',
        ),
        HowToStep(
            title='The Template',
            description='Use data-bind to connect input to a signal, and data-on with debounce to trigger searches:',
            code="""<input
  type="text"
  placeholder="Search contacts..."
  data-bind:search="$search.value"
  data-on:input__debounce.200ms="@get('/active-search/search/')"
>""",
            language='html',
        ),
        HowToStep(
            title='The Fragment',
            description='Return an HTML fragment that Datastar merges into the DOM using fragment IDs:',
            code="""<div id="results">
  {% for contact in contacts %}
  <div id="contact-{{ contact.pk }}">
    {{ contact.first_name }} {{ contact.last_name }}
  </div>
  {% endfor %}
</div>""",
            language='html',
        ),
    ]


def build_click_to_load_steps() -> list[HowToStep]:
    """Build steps for Click to Load example."""
    return [
        HowToStep(
            title='The View',
            description='Create a paginated view that returns SSE with append mode:',
            code=extract_view_code(views.click_to_load_view),
            language='python',
        ),
        HowToStep(
            title='The URL',
            description='Add routes for the main view and load-more endpoint:',
            code="""path('click-to-load/', views.click_to_load_view, name='click-to-load'),
path('click-to-load/more/', views.click_to_load_more_view, name='click-to-load-more'),""",
            language='python',
        ),
        HowToStep(
            title='The Template',
            description='Use data-on:click to trigger loading more items:',
            code="""<div id="contact-list">
  {% for contact in contacts %}
  <div id="contact-{{ contact.pk }}">{{ contact.name }}</div>
  {% endfor %}
</div>

<button
  data-on:click="@get('/click-to-load/more/')"
  data-bind:page="$page"
>
  Load More
</button>""",
            language='html',
        ),
    ]


# Build example configurations with auto-generated steps
EXAMPLES: dict[str, HowToExample] = {
    'active-search': HowToExample(
        slug='active-search',
        title='Active Search',
        description='Search a contacts database as you type with debounced input',
        steps=build_active_search_steps(),
        doc_links=[
            {
                'title': 'Understanding Signals',
                'url': '/docs/datastar-guide/core-concepts.md#signals',
            },
            {
                'title': 'Debouncing Input Events',
                'url': '/docs/datastar-guide/best-practices.md#7-debounce-input-events',
            },
            {
                'title': 'Server-Sent Events (SSE)',
                'url': '/docs/datastar-guide/core-concepts.md#sse-events',
            },
        ],
    ),
    'click-to-load': HowToExample(
        slug='click-to-load',
        title='Click to Load',
        description='Load more content on demand with pagination',
        steps=build_click_to_load_steps(),
        doc_links=[],
    ),
    'edit-row': HowToExample(
        slug='edit-row',
        title='Edit Row',
        description='Inline editing of table rows with instant updates',
        steps=[
            HowToStep(
                title='The View',
                description='Create a view that handles both page render and row updates:',
                code=extract_view_code(views.edit_row_view),
                language='python',
            ),
            HowToStep(
                title='The URL',
                description='Add routes for edit view and update endpoint:',
                code="""path('edit-row/', views.edit_row_view, name='edit-row'),
path('edit-row/update/', views.edit_row_update_view, name='edit-row-update'),""",
                language='python',
            ),
        ],
        doc_links=[],
    ),
    'delete-row': HowToExample(
        slug='delete-row',
        title='Delete Row',
        description='Remove rows with confirmation and animation',
        steps=[
            HowToStep(
                title='The View',
                description='Handle row deletion and return remove directive:',
                code=extract_view_code(views.delete_row_view),
                language='python',
            ),
        ],
        doc_links=[],
    ),
    'todo-mvc': HowToExample(
        slug='todo-mvc',
        title='TodoMVC',
        description='Full CRUD Todo application with localStorage persistence',
        steps=[
            HowToStep(
                title='The Model',
                description='Define a Todo model with ordering:',
                code="""class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']""",
                language='python',
            ),
            HowToStep(
                title='The Views',
                description='Create views for add, toggle, delete operations:',
                code='# See views.py for complete implementation',
                language='python',
            ),
        ],
        doc_links=[],
    ),
    'inline-validation': HowToExample(
        slug='inline-validation',
        title='Inline Validation',
        description='Real-time form validation with server-side feedback',
        steps=[
            HowToStep(
                title='The Form',
                description='Create a Django form with validators:',
                code="""class ContactForm(forms.Form):
    email = forms.EmailField(
        validators=[validate_email]
    )
    name = forms.CharField(max_length=100)""",
                language='python',
            ),
        ],
        doc_links=[],
    ),
    'infinite-scroll': HowToExample(
        slug='infinite-scroll',
        title='Infinite Scroll',
        description='Lazy loading of content as user scrolls',
        steps=[
            HowToStep(
                title='The View',
                description='Return paginated content with SSE:',
                code=extract_view_code(views.infinite_scroll_view),
                language='python',
            ),
        ],
        doc_links=[],
    ),
    'lazy-tabs': HowToExample(
        slug='lazy-tabs',
        title='Lazy Tabs',
        description='Tab content loaded on demand',
        steps=[
            HowToStep(
                title='The View',
                description='Load tab content on request:',
                code=extract_view_code(views.lazy_tabs_view),
                language='python',
            ),
        ],
        doc_links=[],
    ),
    'file-upload': HowToExample(
        slug='file-upload',
        title='File Upload',
        description='Drag and drop file uploads with progress',
        steps=[
            HowToStep(
                title='The View',
                description='Handle file upload via POST:',
                code=extract_view_code(views.file_upload_view),
                language='python',
            ),
        ],
        doc_links=[],
    ),
    'sortable': HowToExample(
        slug='sortable',
        title='Sortable',
        description='Drag and drop reordering with server sync',
        steps=[
            HowToStep(
                title='The View',
                description='Handle reorder POST and return updated order:',
                code=extract_view_code(views.sortable_view),
                language='python',
            ),
        ],
        doc_links=[],
    ),
    'notifications': HowToExample(
        slug='notifications',
        title='Notifications',
        description='Real-time notifications with SSE updates',
        steps=[
            HowToStep(
                title='The View',
                description='Use SSE generator for real-time updates:',
                code=extract_view_code(views.notifications_view),
                language='python',
            ),
        ],
        doc_links=[],
    ),
    'bulk-update': HowToExample(
        slug='bulk-update',
        title='Bulk Update',
        description='Select and update multiple records at once',
        steps=[
            HowToStep(
                title='The View',
                description='Process bulk update form data:',
                code=extract_view_code(views.bulk_update_view),
                language='python',
            ),
        ],
        doc_links=[],
    ),
    'system-messages': HowToExample(
        slug='system-messages',
        title='System Messages',
        description='User feedback messages (success, error, info)',
        steps=[
            HowToStep(
                title='The View',
                description='Handle message display:',
                code=extract_view_code(views.system_messages_view),
                language='python',
            ),
        ],
        doc_links=[],
    ),
}


def get_example(slug: str) -> Optional[HowToExample]:
    """Get HowTo configuration for an example by slug."""
    return EXAMPLES.get(slug)


def get_all_examples() -> list[HowToExample]:
    """Get all example configurations."""
    return list(EXAMPLES.values())


def refresh_example(slug: str) -> HowToExample:
    """Regenerate an example's steps from current code."""
    example = EXAMPLES.get(slug)
    if example:
        # Rebuild steps from current code
        if slug == 'active-search':
            example.steps = build_active_search_steps()
        elif slug == 'click-to-load':
            example.steps = build_click_to_load_steps()
    return example
