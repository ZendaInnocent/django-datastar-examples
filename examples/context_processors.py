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
        },  # Homepage - no breadcrumbs
        'examples:active-search': {'title': 'Active Search', 'show_breadcrumbs': True},
        'examples:click-to-load': {'title': 'Click to Load', 'show_breadcrumbs': True},
        'examples:edit-row': {'title': 'Edit Row', 'show_breadcrumbs': True},
        'examples:delete-row': {'title': 'Delete Row', 'show_breadcrumbs': True},
        'examples:todo-mvc': {'title': 'TodoMVC', 'show_breadcrumbs': True},
        'examples:inline-validation': {
            'title': 'Inline Validation',
            'show_breadcrumbs': True,
        },
        'examples:infinite-scroll': {
            'title': 'Infinite Scroll',
            'show_breadcrumbs': True,
        },
        'examples:lazy-tabs': {'title': 'Lazy Tabs', 'show_breadcrumbs': True},
        'examples:file-upload': {'title': 'File Upload', 'show_breadcrumbs': True},
        'examples:sortable': {'title': 'Sortable', 'show_breadcrumbs': True},
        'examples:notifications': {'title': 'Notifications', 'show_breadcrumbs': True},
        'examples:bulk-update': {'title': 'Bulk Update', 'show_breadcrumbs': True},
    }

    # Try to match current path to a known route
    current_page_name = None
    show_breadcrumbs = False

    # Check if path matches any known example route
    for url_name, config in example_routes.items():
        try:
            resolved_path = reverse(url_name)
            if resolved_path == path:
                current_page_name = config.get('title')
                show_breadcrumbs = config.get('show_breadcrumbs', False)
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
    }
