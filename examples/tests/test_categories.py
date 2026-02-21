"""Tests for example categories feature."""

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

    def test_responsive_grid_classes_present(self):
        """Verify responsive grid classes are present."""
        client = Client()
        response = client.get('/')
        content = response.content.decode('utf-8')

        # Check for responsive grid classes
        assert 'col-md-6 col-lg-4' in content  # 2 cols tablet, 3 cols desktop
