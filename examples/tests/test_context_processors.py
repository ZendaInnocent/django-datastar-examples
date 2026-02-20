"""
Tests for context processors in examples app.

Tests breadcrumbs_context including:
- Basic function existence
- Context structure
- Return types
"""

from django.test import RequestFactory

from examples.context_processors import breadcrumbs_context


class TestBreadcrumbsContextProcessor:
    """Tests for breadcrumbs_context."""

    def test_context_returns_dict(self):
        """Context returns a dictionary."""
        factory = RequestFactory()
        request = factory.get('/')
        request.session = {}

        context = breadcrumbs_context(request)
        assert isinstance(context, dict)

    def test_context_has_required_keys(self):
        """Context has all required keys."""
        factory = RequestFactory()
        request = factory.get('/')
        request.session = {}

        context = breadcrumbs_context(request)
        assert 'current_page_name' in context
        assert 'show_breadcrumbs' in context
        assert 'howto_slug' in context
        assert 'howto_title' in context

    def test_index_returns_correct_keys(self):
        """Index path returns expected keys."""
        factory = RequestFactory()
        request = factory.get('/')
        request.session = {}

        context = breadcrumbs_context(request)
        assert 'current_page_name' in context
        assert 'show_breadcrumbs' in context
        assert 'howto_slug' in context
        assert 'howto_title' in context

    def test_example_path_returns_correct_keys(self):
        """Example paths return expected keys."""
        factory = RequestFactory()
        request = factory.get('/active-search/')
        request.session = {}

        context = breadcrumbs_context(request)
        assert 'current_page_name' in context
        assert 'show_breadcrumbs' in context

    def test_unknown_path_returns_correct_keys(self):
        """Unknown paths return expected keys."""
        factory = RequestFactory()
        request = factory.get('/unknown/')
        request.session = {}

        context = breadcrumbs_context(request)
        assert 'current_page_name' in context
        assert 'show_breadcrumbs' in context
