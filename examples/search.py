"""
Search functionality for Django Datastar Examples.

This module provides an in-memory search index using Django Q objects
for filtering and relevance ranking.

Auto-discovery:
    Examples are auto-discovered from EXAMPLES_DATA below. To add a new example:
    1. Add entry to EXAMPLES_DATA with id, title, description, url, category
    2. The search index will automatically include it
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from django.db.models import Q

# Build paths inside the project - go up to project root
# examples/search.py -> examples/ -> project root
BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / 'docs' / 'datastar-guide'


@dataclass
class SearchIndexEntry:
    """Represents a single entry in the search index."""

    title: str
    description: str
    content: str
    url: str
    type: str  # "example" | "doc"
    category: str
    learn_more_url: Optional[str] = None  # Link to docs (for examples)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for template rendering."""
        result = {
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'type': self.type,
            'category': self.category,
        }
        if self.learn_more_url:
            result['learn_more_url'] = self.learn_more_url
        return result

    def get_q_field_value(self, field_name: str) -> str:
        """
        Get field value for Q object compatibility.

        This method allows SearchIndexEntry to work with Django Q objects
        by mapping field names to attribute values.

        Args:
            field_name: Name of the field (title, description, content)

        Returns:
            Field value as string
        """
        field_map = {
            'title': self.title,
            'description': self.description,
            'content': self.content,
        }
        return field_map.get(field_name, '')


# Example data with full searchable content
EXAMPLES_DATA = [
    {
        'id': 'active-search',
        'title': 'Active Search',
        'description': 'Real-time search with instant results as you type',
        'content': 'Active Search example demonstrating real-time search functionality using Datastar. Shows how to implement instant search with Server-Sent Events and Django Q objects for filtering database queries.',
        'url': '/active-search/',
        'category': 'Search',
    },
    {
        'id': 'click-to-load',
        'title': 'Click to Load',
        'description': 'Load more content on button click with progressive loading',
        'content': 'Click to Load example showing progressive loading pattern. Demonstrates lazy loading content on button click using Datastar fragments and Server-Sent Events for dynamic DOM updates.',
        'url': '/click-to-load/',
        'category': 'Interactive',
    },
    {
        'id': 'edit-row',
        'title': 'Edit Row',
        'description': 'Inline editing of table rows with immediate feedback',
        'content': 'Edit Row example for inline table editing. Shows how to implement inline editing with immediate visual feedback using Datastar patch_elements and Django form handling.',
        'url': '/edit-row/',
        'category': 'CRUD',
    },
    {
        'id': 'delete-row',
        'title': 'Delete Row',
        'description': 'Remove rows with confirmation and visual feedback',
        'content': 'Delete Row example demonstrating row deletion with visual feedback. Implements Datastar remove_elements for smooth DOM removal after database deletion.',
        'url': '/delete-row/',
        'category': 'CRUD',
    },
    {
        'id': 'todo-mvc',
        'title': 'TodoMVC',
        'description': 'Full todo application with add, toggle, and delete functionality',
        'content': 'TodoMVC example showing complete todo application. Implements add, toggle, complete, and delete functionality using Datastar Server-Sent Events for real-time updates.',
        'url': '/todo-mvc/',
        'category': 'Interactive',
    },
    {
        'id': 'inline-validation',
        'title': 'Inline Validation',
        'description': 'Real-time form validation with instant feedback',
        'content': 'Inline Validation example demonstrates real-time form field validation. Shows how to validate email, username, and password fields with instant feedback using Datastar.',
        'url': '/inline-validation/',
        'category': 'Interactive',
    },
    {
        'id': 'infinite-scroll',
        'title': 'Infinite Scroll',
        'description': 'Automatically load more content as you scroll',
        'content': 'Infinite Scroll example implementing automatic content loading on scroll. Uses Datastar to load and append new items seamlessly without page refresh.',
        'url': '/infinite-scroll/',
        'category': 'Real-time',
    },
    {
        'id': 'lazy-tabs',
        'title': 'Lazy Tabs',
        'description': 'Tabbed interface with lazy-loaded content',
        'content': 'Lazy Tabs example demonstrates tabbed navigation with lazy-loaded content. Shows how to load tab content dynamically using Datastar fragments.',
        'url': '/lazy-tabs/',
        'category': 'Interactive',
    },
    {
        'id': 'file-upload',
        'title': 'File Upload',
        'description': 'File upload with progress indication and feedback',
        'content': 'File Upload example showing file upload handling with Datastar. Demonstrates file upload, progress indication, and server-side processing.',
        'url': '/file-upload/',
        'category': 'Interactive',
    },
    {
        'id': 'sortable',
        'title': 'Sortable',
        'description': 'Drag and drop reordering of items',
        'content': 'Sortable example implementing drag and drop reordering. Shows how to handle drag events and update item order in the database using Datastar.',
        'url': '/sortable/',
        'category': 'Interactive',
    },
    {
        'id': 'notifications',
        'title': 'Notifications',
        'description': 'Real-time notification system with count updates',
        'content': 'Notifications example demonstrating real-time notification system. Shows how to implement notification count updates and mark-as-read functionality using Datastar signals.',
        'url': '/notifications/',
        'category': 'Real-time',
    },
    {
        'id': 'bulk-update',
        'title': 'Bulk Update',
        'description': 'Select and update multiple items at once',
        'content': 'Bulk Update example for selecting and updating multiple items. Demonstrates batch operations with Datastar for efficient bulk delete and update operations.',
        'url': '/bulk-update/',
        'category': 'CRUD',
    },
]

# Routes to exclude from auto-discovery (exact matches only)
# These are child routes, API endpoints, and utility routes
EXCLUDED_NAMES = frozenset(
    (
        'index',
        'search',
        'search-instant',
        'get-contact',
    )
)


def _kebab_to_title(name: str) -> str:
    """Convert kebab-case to Title Case."""
    return ' '.join(word.capitalize() for word in name.replace('-', ' ').split())


def auto_discover_examples() -> List[Dict[str, str]]:
    """
    Auto-discover examples from urls.py using Django's reverse().

    This function uses Django's URL resolver to get exact paths.
    For each URL:
    - Uses reverse() to get exact URL path
    - Generates title from URL name (e.g., 'active-search' -> 'Active Search')
    - Uses description from EXAMPLES_DATA if available
    - Falls back to placeholder if not

    Returns:
        List of example dictionaries with id, title, description, url, category
    """
    from django.urls import reverse

    example_ids = {item['id'] for item in EXAMPLES_DATA}
    discovered = []

    # Get all URL patterns from examples.urls
    from examples import urls

    for pattern in urls.urlpatterns:
        name = pattern.name
        if not name:
            continue

        # Skip exact excluded names
        if name in EXCLUDED_NAMES:
            continue

        # Skip child routes (names with multiple hyphens that aren't in EXAMPLES_DATA)
        # e.g., 'todo-mvc-toggle', 'todo-mvc-delete' are child routes
        # But 'active-search' is a main route (single hyphen is OK)
        if '-' in name and name not in example_ids:
            continue

        # Get URL path using Django's reverse
        try:
            url_path = reverse(f'examples:{name}')
        except Exception:
            continue

        # Check if we have rich data in EXAMPLES_DATA
        if name in example_ids:
            existing = next(item for item in EXAMPLES_DATA if item['id'] == name)
            # Update URL with exact path from reverse
            existing = existing.copy()
            existing['url'] = url_path
            # Add learn_more link to docs
            existing['learn_more_url'] = f'/docs/{name}/'
            discovered.append(existing)
        else:
            # Auto-generate entry
            discovered.append(
                {
                    'id': name,
                    'title': _kebab_to_title(name),
                    'description': f'Example: {_kebab_to_title(name)}',
                    'content': f'Example demonstrating {_kebab_to_title(name).lower()} with Datastar.',
                    'url': url_path,
                    'category': 'Auto-discovered',
                    'learn_more_url': f'/docs/{name}/',
                }
            )

    return discovered


# Auto-discovered examples (combines manual + discovered)
# To update: run auto_discover_examples() and merge with EXAMPLES_DATA
AUTO_DISCOVERED_EXAMPLES = auto_discover_examples()


def _load_docs_data() -> List[Dict[str, str]]:
    """Load documentation data from markdown files."""
    docs = []

    if not DOCS_DIR.exists():
        return docs

    # Mapping of doc slugs to titles and URLs
    doc_mapping = {
        'index': {'title': 'Datastar Guide', 'url': '/docs/'},
        'table-of-contents': {
            'title': 'Table of Contents',
            'url': '/docs/table-of-contents/',
        },
        'core-concepts': {'title': 'Core Concepts', 'url': '/docs/core-concepts/'},
        'django-integration': {
            'title': 'Django Integration',
            'url': '/docs/django-integration/',
        },
        'best-practices': {'title': 'Best Practices', 'url': '/docs/best-practices/'},
        'common-patterns': {
            'title': 'Common Patterns',
            'url': '/docs/common-patterns/',
        },
        'installation': {'title': 'Installation', 'url': '/docs/installation/'},
        'troubleshooting': {
            'title': 'Troubleshooting',
            'url': '/docs/troubleshooting/',
        },
        'version-compatibility': {
            'title': 'Version Compatibility',
            'url': '/docs/version-compatibility/',
        },
        'python-sdk-api': {'title': 'Python SDK API', 'url': '/docs/python-sdk-api/'},
        'django-forms-integration': {
            'title': 'Django Forms Integration',
            'url': '/docs/django-forms-integration/',
        },
        'datastar-attributes-reference': {
            'title': 'Datastar Attributes Reference',
            'url': '/docs/datastar-attributes-reference/',
        },
        'datastar-actions-reference': {
            'title': 'Datastar Actions Reference',
            'url': '/docs/datastar-actions-reference/',
        },
        'error-handling': {'title': 'Error Handling', 'url': '/docs/error-handling/'},
    }

    for doc_file in DOCS_DIR.glob('*.md'):
        slug = doc_file.stem
        if slug.startswith('index'):
            slug = 'index'

        mapping = doc_mapping.get(
            slug, {'title': slug.replace('-', ' ').title(), 'url': f'/docs/{slug}/'}
        )

        try:
            content = doc_file.read_text(encoding='utf-8')
            # Extract first paragraph as description
            lines = content.split('\n')
            description = ''
            for line in lines[1:]:  # Skip title line
                line = line.strip()
                if line and not line.startswith('#'):
                    description = line[:150]
                    if len(line) > 150:
                        description += '...'
                    break
        except (OSError, UnicodeDecodeError):
            content = ''
            description = ''

        docs.append(
            {
                'id': f'docs-{slug}',
                'title': mapping['title'],
                'description': description or f'Documentation for {mapping["title"]}',
                'content': content,
                'url': mapping['url'],
                'category': 'Documentation',
            }
        )

    return docs


# Docs are for agents only - disabled for user search
# To enable: uncomment the line below
# DOCS_DATA = _load_docs_data()
DOCS_DATA: List[Dict[str, str]] = []


class SearchIndex:
    """
    In-memory search index using Django Q objects for filtering.

    Relevance ranking:
    - Priority 1: Title contains query (highest)
    - Priority 2: Description contains query
    - Priority 3: Content contains query (lowest)
    """

    def __init__(self):
        self.entries: List[SearchIndexEntry] = []
        self._build_index()

    def _build_index(self):
        """Build the search index from examples and documentation."""
        # Index examples (auto-discovered from urls.py + EXAMPLES_DATA)
        for item in AUTO_DISCOVERED_EXAMPLES:
            self.entries.append(
                SearchIndexEntry(
                    title=item['title'],
                    description=item['description'],
                    content=item.get('content', ''),
                    url=item['url'],
                    type='example',
                    category=item['category'],
                    learn_more_url=item.get('learn_more_url'),
                )
            )

        # Index documentation
        for item in DOCS_DATA:
            self.entries.append(
                SearchIndexEntry(
                    title=item['title'],
                    description=item['description'],
                    content=item.get('content', ''),
                    url=item['url'],
                    type='doc',
                    category=item['category'],
                )
            )

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search using Django Q objects with relevance ranking.

        Uses Q objects to filter entries by title, description, and content
        with case-insensitive matching. Results are ranked by relevance:
        title matches > description matches > content matches.

        Args:
            query: Search query string
            limit: Maximum number of results to return

        Returns:
            List of matching results sorted by relevance
        """
        if not query:
            return []

        # Create QEntry objects for case-insensitive contains matching
        # QEntry extends Django Q objects to work with in-memory SearchIndexEntry
        title_q, desc_q, content_q = create_search_q(query)

        # Score each entry based on QEntry object matching with relevance ranking
        scored_results: List[tuple] = []

        for entry in self.entries:
            score = 0
            match_type = 0  # 0=no match, 1=content, 2=description, 3=title

            # Check title match using QEntry object (highest priority - score 100)
            if title_q.check(entry):
                score += 100
                match_type = 3
                # Bonus for exact title start match
                if entry.title.lower().startswith(query.lower()):
                    score += 20

            # Check description match using QEntry object (medium priority - score 50)
            if desc_q.check(entry):
                score += 50
                if match_type < 2:
                    match_type = 2

            # Check content match using QEntry object (lowest priority - score 25)
            if content_q.check(entry):
                score += 25
                if match_type < 1:
                    match_type = 1

            # Only include if there's a match
            if score > 0:
                scored_results.append((score, match_type, entry))

        # Sort by score (descending), then by match_type (ascending), then alphabetically
        scored_results.sort(key=lambda x: (-x[0], x[1], x[2].title))

        # Convert to dict format for template
        return [entry.to_dict() for _, _, entry in scored_results[:limit]]

    def get_all_entries(self) -> List[SearchIndexEntry]:
        """Return all entries in the index."""
        return self.entries

    def rebuild(self):
        """Rebuild the search index."""
        self.entries = []
        self._build_index()


# Extend Q object to support in-memory dataclass filtering
class QEntry(Q):
    """
    Extended Q object that supports checking against SearchIndexEntry dataclasses.

    This extends Django's Q object to work with in-memory search index entries,
    enabling the use of Q object patterns for filtering without database queries.
    """

    def check(self, entry: SearchIndexEntry) -> bool:
        """
        Check if a SearchIndexEntry matches this Q object condition.

        Supports __icontains lookup for title, description, and content fields.

        Args:
            entry: SearchIndexEntry to check against

        Returns:
            True if entry matches the condition, False otherwise
        """
        # Get the field name and lookup type from the Q object
        for field_lookup, value in self.children:
            if isinstance(field_lookup, str):
                if '__' in field_lookup:
                    field_name, lookup = field_lookup.split('__', 1)
                else:
                    field_name, lookup = field_lookup, 'exact'

                field_value = entry.get_q_field_value(field_name)

                if lookup == 'icontains':
                    if value.lower() not in field_value.lower():
                        return False
                elif lookup == 'contains':
                    if value not in field_value:
                        return False
                elif lookup == 'exact':
                    if field_value != value:
                        return False
                elif lookup == 'iexact':
                    if field_value.lower() != value.lower():
                        return False

        return True


def create_search_q(query: str) -> tuple:
    """
    Create QEntry objects for search filtering.

    Creates Q objects for title, description, and content fields
    with case-insensitive contains lookup.

    Args:
        query: Search query string

    Returns:
        Tuple of (title_q, desc_q, content_q) QEntry objects
    """
    title_q = QEntry(title__icontains=query)
    desc_q = QEntry(description__icontains=query)
    content_q = QEntry(content__icontains=query)
    return title_q, desc_q, content_q


# Global search index instance
_search_index: Optional[SearchIndex] = None


def get_search_index() -> SearchIndex:
    """Get or create the global search index instance."""
    global _search_index
    if _search_index is None:
        _search_index = SearchIndex()
    return _search_index


def rebuild_search_index() -> SearchIndex:
    """Rebuild and return the search index."""
    global _search_index
    _search_index = SearchIndex()
    return _search_index


def search(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Convenience function to search the index.

    Args:
        query: Search query string
        limit: Maximum number of results to return

    Returns:
        List of matching results sorted by relevance
    """
    index = get_search_index()
    return index.search(query, limit)
