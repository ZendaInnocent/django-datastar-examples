"""
Tests for Copy Code Functionality (Story 2.2)

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


class TestCopyButtonHTMLStructure:
    """Test the HTML structure of the copy button template include."""

    def test_code_block_include_exists(self):
        """Verify the code_block.html include template exists."""
        from django.template.loader import get_template

        try:
            get_template('includes/code_block.html')
            # Template exists and can be loaded
            assert True
        except Exception as e:
            pytest.fail(f'Could not load code_block.html template: {e}')

    def test_copy_button_has_aria_label(self):
        """Verify copy button includes accessibility label."""
        from django.template.loader import render_to_string

        rendered = render_to_string(
            'includes/code_block.html',
            {'language': 'python', 'code': 'print("hello")', 'code_id': 'test-code'},
        )
        assert 'aria-label' in rendered
        assert 'Copy code to clipboard' in rendered

    def test_copy_button_has_data_attribute(self):
        """Verify copy button has data-code-id attribute."""
        from django.template.loader import render_to_string

        rendered = render_to_string(
            'includes/code_block.html',
            {'language': 'python', 'code': 'print("hello")', 'code_id': 'test-code-id'},
        )
        assert 'data-code-id' in rendered
        assert 'test-code-id' in rendered


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
