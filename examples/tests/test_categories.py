"""Tests for example categories feature (Story 1.2)."""

import pytest
from django.test import Client


pytestmark = pytest.mark.django_db


class TestExampleCategories:
    """Test cases for example category organization."""

    def test_index_page_loads_successfully(self):
        """Verify index page loads without errors."""
        client = Client()
        response = client.get('/')
        assert response.status_code == 200

    def test_all_12_examples_have_category_badges(self):
        """Verify all 12 examples have category badges displayed."""
        client = Client()
        response = client.get('/')
        content = response.content.decode('utf-8')

        # Count category badges
        assert content.count('badge bg-primary') >= 1  # Search (blue)
        assert content.count('badge bg-success') >= 3  # CRUD (green) - 3 examples
        assert content.count('#6B46C1') >= 4  # Real-time (purple) - 4 examples
        assert (
            content.count('badge bg-warning') >= 4
        )  # Interactive (orange) - 4 examples

    def test_search_category_has_active_search(self):
        """Verify Search category contains Active Search example."""
        client = Client()
        response = client.get('/')
        content = response.content.decode('utf-8')

        # Active Search should be in Search category
        assert 'Active Search' in content
        # Active Search should have a badge (we're checking badge appears near it)
        assert '<span class="badge bg-primary mb-2">Search</span>' in content

    def test_crud_category_has_correct_examples(self):
        """Verify CRUD category contains Edit Row, Delete Row, Bulk Update."""
        client = Client()
        response = client.get('/')
        content = response.content.decode('utf-8')

        # Check CRUD badge is present
        assert '<span class="badge bg-success mb-2">CRUD</span>' in content

        # Check CRUD examples are present
        assert 'Edit Row' in content
        assert 'Delete Row' in content
        assert 'Bulk Update' in content

    def test_realtime_category_has_correct_examples(self):
        """Verify Real-time category contains correct examples."""
        client = Client()
        response = client.get('/')
        content = response.content.decode('utf-8')

        # Check Real-time badge is present
        assert 'Real-time' in content

        # Check Real-time examples are present
        assert 'Click to Load' in content
        assert 'Inline Validation' in content
        assert 'Infinite Scroll' in content
        assert 'Notifications' in content

    def test_interactive_category_has_correct_examples(self):
        """Verify Interactive category contains correct examples."""
        client = Client()
        response = client.get('/')
        content = response.content.decode('utf-8')

        # Check Interactive badge is present
        assert '<span class="badge bg-warning' in content

        # Check Interactive examples are present
        assert 'TodoMVC' in content
        assert 'Lazy Tabs' in content
        assert 'File Upload' in content
        assert 'Sortable' in content

    def test_category_sections_exist(self):
        """Verify all 4 category sections are present."""
        client = Client()
        response = client.get('/')
        content = response.content.decode('utf-8')

        # Check category headings exist
        assert 'Search' in content
        assert 'CRUD' in content
        assert 'Real-time' in content
        assert 'Interactive' in content

    def test_no_duplicate_examples(self):
        """Verify each example appears only once."""
        client = Client()
        response = client.get('/')
        content = response.content.decode('utf-8')

        # Count each example name - should appear exactly once
        examples = [
            'Active Search',
            'Click to Load',
            'Edit Row',
            'Delete Row',
            'TodoMVC',
            'Inline Validation',
            'Infinite Scroll',
            'Lazy Tabs',
            'File Upload',
            'Sortable',
            'Notifications',
            'Bulk Update',
        ]

        for example in examples:
            assert content.count(example) == 1, f'{example} should appear exactly once'

    def test_responsive_grid_classes_present(self):
        """Verify responsive grid classes are present."""
        client = Client()
        response = client.get('/')
        content = response.content.decode('utf-8')

        # Check for responsive grid classes
        assert 'col-md-6 col-lg-4' in content  # 2 cols tablet, 3 cols desktop
