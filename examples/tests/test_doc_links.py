"""Tests for example documentation links feature (Story 1.3)."""

import pytest
from django.test import Client


pytestmark = pytest.mark.django_db


# The 12 examples to test
EXAMPLES = [
    ('active-search/', 'Active Search'),
    ('click-to-load/', 'Click to Load'),
    ('edit-row/', 'Edit Row'),
    ('delete-row/', 'Delete Row'),
    ('todo-mvc/', 'TodoMVC'),
    ('inline-validation/', 'Inline Validation'),
    ('infinite-scroll/', 'Infinite Scroll'),
    ('lazy-tabs/', 'Lazy Tabs'),
    ('file-upload/', 'File Upload'),
    ('sortable/', 'Sortable'),
    ('notifications/', 'Notifications'),
    ('bulk-update/', 'Bulk Update'),
]


class TestExampleDocumentationLinks:
    """Test cases for example documentation links feature."""

    def test_index_page_loads_successfully(self):
        """Verify index page loads without errors."""
        client = Client()
        response = client.get('/')
        assert response.status_code == 200

    @pytest.mark.parametrize('url,title', EXAMPLES)
    def test_example_page_has_learn_more_section(self, url, title):
        """Verify each example page has a 'Learn More' section with documentation links."""
        client = Client()
        response = client.get(f'/{url}')
        assert response.status_code == 200, f'Failed to load {title}'
        content = response.content.decode('utf-8')

        # Check for "Learn More" section
        assert 'Learn More' in content, f"{title} should have 'Learn More' section"
        # Check for card with documentation links
        assert '<h2 class="h5 mb-3">Learn More</h2>' in content, (
            f'{title} should have Learn More heading'
        )

    @pytest.mark.parametrize('url,title', EXAMPLES)
    def test_example_page_has_documentation_links(self, url, title):
        """Verify each example page has at least 2 documentation links."""
        client = Client()
        response = client.get(f'/{url}')
        assert response.status_code == 200, f'Failed to load {title}'
        content = response.content.decode('utf-8')

        # Count anchor tags in Learn More section (should have at least 2)
        # We look for links after the Learn More heading
        learn_more_start = content.find('Learn More')
        if learn_more_start > 0:
            learn_more_section = content[learn_more_start:]
            # Count anchor tags in this section
            link_count = learn_more_section.count('<a href=')
            assert link_count >= 2, (
                f'{title} should have at least 2 documentation links, found {link_count}'
            )

    @pytest.mark.parametrize('url,title', EXAMPLES)
    def test_example_page_links_use_datastar_purple(self, url, title):
        """Verify all documentation links use Datastar Purple (#6B46C1) color."""
        client = Client()
        response = client.get(f'/{url}')
        assert response.status_code == 200, f'Failed to load {title}'
        content = response.content.decode('utf-8')

        # Check that links use the Datastar Purple color
        # Looking for style="color: #6B46C1" in anchor tags within Learn More section
        learn_more_start = content.find('Learn More')
        if learn_more_start > 0:
            learn_more_section = content[
                learn_more_start : learn_more_start + 2000
            ]  # Look in first 2000 chars
            # Check for the purple color in links
            assert '#6B46C1' in learn_more_section or '6B46C1' in learn_more_section, (
                f'{title} documentation links should use Datastar Purple (#6B46C1)'
            )

    @pytest.mark.parametrize('url,title', EXAMPLES)
    def test_example_page_links_open_in_same_window(self, url, title):
        """Verify documentation links open in same window (no target='_blank')."""
        client = Client()
        response = client.get(f'/{url}')
        assert response.status_code == 200, f'Failed to load {title}'
        content = response.content.decode('utf-8')

        # Check that Learn More section doesn't have target="_blank"
        learn_more_start = content.find('Learn More')
        if learn_more_start > 0:
            learn_more_section = content[learn_more_start : learn_more_start + 2000]
            # Should NOT have target="_blank"
            assert 'target="_blank"' not in learn_more_section, (
                f"{title} documentation links should NOT have target='_blank'"
            )

    def test_active_search_example_documentation_links(self):
        """Verify Active Search example has relevant documentation links."""
        client = Client()
        response = client.get('/active-search/')
        assert response.status_code == 200
        content = response.content.decode('utf-8')

        # Active Search should have links to signals, debounce, SSE documentation
        learn_more_start = content.find('Learn More')
        if learn_more_start > 0:
            learn_more_section = content[learn_more_start : learn_more_start + 1500]
            # Should mention relevant topics for Active Search
            assert 'Signals' in learn_more_section or 'signals' in learn_more_section

    def test_crud_examples_have_form_documentation_links(self):
        """Verify CRUD examples have links to form handling documentation."""
        client = Client()

        for url, title in [
            ('edit-row/', 'Edit Row'),
            ('delete-row/', 'Delete Row'),
            ('bulk-update/', 'Bulk Update'),
        ]:
            response = client.get(f'/{url}')
            assert response.status_code == 200, f'Failed to load {title}'
            content = response.content.decode('utf-8')

            learn_more_start = content.find('Learn More')
            if learn_more_start > 0:
                learn_more_section = content[learn_more_start : learn_more_start + 1500]
                # CRUD-related docs
                assert (
                    'form' in learn_more_section.lower() or 'Form' in learn_more_section
                ), f'{title} should have form-related documentation'

    def test_realtime_examples_have_sse_documentation_links(self):
        """Verify real-time examples have links to SSE documentation."""
        client = Client()

        for url, title in [
            ('click-to-load/', 'Click to Load'),
            ('notifications/', 'Notifications'),
        ]:
            response = client.get(f'/{url}')
            assert response.status_code == 200, f'Failed to load {title}'
            content = response.content.decode('utf-8')

            learn_more_start = content.find('Learn More')
            if learn_more_start > 0:
                learn_more_section = content[learn_more_start : learn_more_start + 1500]
                # Real-time examples should have SSE or real-time related docs
                assert (
                    'SSE' in learn_more_section
                    or 'real-time' in learn_more_section.lower()
                    or 'Real' in learn_more_section
                )
