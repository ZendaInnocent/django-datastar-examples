"""
Tests for Copy Code Functionality

This module tests the JavaScript copy-to-clipboard functionality
by verifying the HTML structure and JavaScript integration.
"""

import pytest
from django.test import Client


@pytest.mark.django_db
class TestCopyCodeFunctionality:
    """Test cases for copy code functionality."""

    def test_base_template_has_toast_container(self):
        """Verify base template includes toast container for notifications."""
        client = Client()
        response = client.get('/')
        assert response.status_code == 200
        # Check toast container is present
        assert 'class="toast-container"' in response.content.decode()

    def test_base_template_has_code_blocks_js(self):
        """Verify base template includes the code-blocks.js script."""
        client = Client()
        response = client.get('/')
        assert response.status_code == 200
        # Check custom JS is loaded
        assert 'code-blocks.js' in response.content.decode()

    def test_base_template_has_custom_css(self):
        """Verify base template includes custom CSS."""
        client = Client()
        response = client.get('/')
        assert response.status_code == 200
        # Check custom CSS is loaded
        assert 'custom.css' in response.content.decode()

    def test_custom_css_file_is_loaded(self):
        """Verify custom CSS file is loaded via static URL."""
        client = Client()
        response = client.get('/')
        assert response.status_code == 200
        # The custom CSS should be referenced in the HTML
        assert b'/static/css/custom.css' in response.content

    def test_code_blocks_js_is_loaded(self):
        """Verify code-blocks.js file is loaded via static URL."""
        client = Client()
        response = client.get('/')
        assert response.status_code == 200
        # The JS file should be referenced in the HTML
        assert b'/static/js/code-blocks.js' in response.content


class TestStaticFilesConfiguration:
    """Test that static files are properly configured."""

    def test_staticfiles_dirs_configured(self):
        """Verify STATICFILES_DIRS is configured."""
        from django.conf import settings

        assert hasattr(settings, 'STATICFILES_DIRS')
        assert 'static' in [str(d.name) for d in settings.STATICFILES_DIRS]

    def test_custom_css_file_exists(self):
        """Verify custom CSS file exists."""
        from django.conf import settings

        static_path = settings.BASE_DIR / 'static' / 'css' / 'custom.css'
        assert static_path.exists(), f'custom.css not found at {static_path}'

    def test_code_blocks_js_file_exists(self):
        """Verify code-blocks.js file exists."""
        from django.conf import settings

        static_path = settings.BASE_DIR / 'static' / 'js' / 'code-blocks.js'
        assert static_path.exists(), f'code-blocks.js not found at {static_path}'
