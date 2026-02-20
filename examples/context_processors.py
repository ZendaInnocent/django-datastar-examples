"""Context processors for examples app."""

import logging

from django.urls import reverse

logger = logging.getLogger(__name__)


def breadcrumbs_context(request):
    """Add breadcrumb context based on current URL."""
    path = request.path

    # Define routes that should show breadcrumbs (example pages)
    # Using URL names for flexibility - more maintainable than hardcoded paths
    example_routes = {
        'examples:index': {
            'title': None,
            'show_breadcrumbs': False,
            'howto_slug': None,
            'howto_title': None,
        },  # Homepage - no breadcrumbs
        'examples:active-search': {
            'title': 'Active Search',
            'show_breadcrumbs': True,
            'howto_slug': 'active-search',
            'howto_title': 'How to Build: Active Search',
        },
        'examples:click-to-load': {
            'title': 'Click to Load',
            'show_breadcrumbs': True,
            'howto_slug': 'click-to-load',
            'howto_title': 'How to Build: Click to Load',
        },
        'examples:edit-row': {
            'title': 'Edit Row',
            'show_breadcrumbs': True,
            'howto_slug': 'edit-row',
            'howto_title': 'How to Build: Edit Row',
        },
        'examples:delete-row': {
            'title': 'Delete Row',
            'show_breadcrumbs': True,
            'howto_slug': 'delete-row',
            'howto_title': 'How to Build: Delete Row',
        },
        'examples:todo-mvc': {
            'title': 'TodoMVC',
            'show_breadcrumbs': True,
            'howto_slug': 'todo-mvc',
            'howto_title': 'How to Build: TodoMVC',
        },
        'examples:inline-validation': {
            'title': 'Inline Validation',
            'show_breadcrumbs': True,
            'howto_slug': 'inline-validation',
            'howto_title': 'How to Build: Inline Validation',
        },
        'examples:infinite-scroll': {
            'title': 'Infinite Scroll',
            'show_breadcrumbs': True,
            'howto_slug': 'infinite-scroll',
            'howto_title': 'How to Build: Infinite Scroll',
        },
        'examples:lazy-tabs': {
            'title': 'Lazy Tabs',
            'show_breadcrumbs': True,
            'howto_slug': 'lazy-tabs',
            'howto_title': 'How to Build: Lazy Tabs',
        },
        'examples:file-upload': {
            'title': 'File Upload',
            'show_breadcrumbs': True,
            'howto_slug': 'file-upload',
            'howto_title': 'How to Build: File Upload',
        },
        'examples:sortable': {
            'title': 'Sortable',
            'show_breadcrumbs': True,
            'howto_slug': 'sortable',
            'howto_title': 'How to Build: Sortable',
        },
        'examples:notifications': {
            'title': 'Notifications',
            'show_breadcrumbs': True,
            'howto_slug': 'notifications',
            'howto_title': 'How to Build: Notifications',
        },
        'examples:bulk-update': {
            'title': 'Bulk Update',
            'show_breadcrumbs': True,
            'howto_slug': 'bulk-update',
            'howto_title': 'How to Build: Bulk Update',
        },
        'examples:system-messages': {
            'title': 'System Messages',
            'show_breadcrumbs': True,
            'howto_slug': 'system-messages',
            'howto_title': 'How to Build: System Messages',
        },
    }

    # Try to match current path to a known route
    current_page_name = None
    show_breadcrumbs = False
    howto_slug = None
    howto_title = None

    # Check if path matches any known example route
    for url_name, config in example_routes.items():
        try:
            resolved_path = reverse(url_name)
            if resolved_path == path:
                current_page_name = config.get('title')
                show_breadcrumbs = config.get('show_breadcrumbs', False)
                howto_slug = config.get('howto_slug')
                howto_title = config.get('howto_title')
                break
        except Exception:
            # URL not found - skip this entry
            pass

    # Fallback: Try to extract page name from path for unknown routes
    if current_page_name is None and show_breadcrumbs is False and path != '/':
        # Log unknown routes for monitoring
        logger.debug(f'Unknown breadcrumb route: {path}')

    return {
        'current_page_name': current_page_name,
        'show_breadcrumbs': show_breadcrumbs,
        'howto_slug': howto_slug,
        'howto_title': howto_title,
    }
