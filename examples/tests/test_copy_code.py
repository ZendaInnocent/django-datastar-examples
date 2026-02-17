"""
Tests for Copy Code Functionality (Story 2.2)

This module tests the JavaScript copy-to-clipboard functionality
by verifying the HTML structure and JavaScript integration.
"""

from django.test import TestCase, Client
from django.urls import reverse


class CopyCodeFunctionalityTests(TestCase):
    """Test cases for copy code functionality."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_base_template_has_toast_container(self):
        """Verify base template includes toast container for notifications."""
        response = self.client.get(reverse('examples:index'))
        self.assertEqual(response.status_code, 200)
        # Check toast container is present
        self.assertContains(response, 'class="toast-container"')

    def test_base_template_has_code_blocks_js(self):
        """Verify base template includes the code-blocks.js script."""
        response = self.client.get(reverse('examples:index'))
        self.assertEqual(response.status_code, 200)
        # Check custom JS is loaded
        self.assertContains(response, 'code-blocks.js')

    def test_base_template_has_custom_css(self):
        """Verify base template includes custom CSS."""
        response = self.client.get(reverse('examples:index'))
        self.assertEqual(response.status_code, 200)
        # Check custom CSS is loaded
        self.assertContains(response, 'custom.css')

    def test_custom_css_file_is_loaded(self):
        """Verify custom CSS file is loaded via static URL."""
        response = self.client.get(reverse('examples:index'))
        self.assertEqual(response.status_code, 200)
        # The custom CSS should be referenced in the HTML
        self.assertIn(b'/static/css/custom.css', response.content)

    def test_code_blocks_js_is_loaded(self):
        """Verify code-blocks.js file is loaded via static URL."""
        response = self.client.get(reverse('examples:index'))
        self.assertEqual(response.status_code, 200)
        # The JS file should be referenced in the HTML
        self.assertIn(b'/static/js/code-blocks.js', response.content)


class CopyButtonHTMLStructureTests(TestCase):
    """Test the HTML structure of the copy button template include."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_code_block_include_exists(self):
        """Verify the code_block.html include template exists."""
        from django.template.loader import get_template

        try:
            get_template('includes/code_block.html')
            # Template exists and can be loaded
            self.assertTrue(True)
        except Exception as e:
            self.fail(f'Could not load code_block.html template: {e}')

    def test_copy_button_has_aria_label(self):
        """Verify copy button includes accessibility label."""
        from django.template.loader import render_to_string

        rendered = render_to_string(
            'includes/code_block.html',
            {'language': 'python', 'code': 'print("hello")', 'code_id': 'test-code'},
        )
        self.assertIn('aria-label', rendered)
        self.assertIn('Copy code to clipboard', rendered)

    def test_copy_button_has_data_attribute(self):
        """Verify copy button has data-code-id attribute."""
        from django.template.loader import render_to_string

        rendered = render_to_string(
            'includes/code_block.html',
            {'language': 'python', 'code': 'print("hello")', 'code_id': 'test-code-id'},
        )
        self.assertIn('data-code-id', rendered)
        self.assertIn('test-code-id', rendered)


class StaticFilesConfigurationTests(TestCase):
    """Test that static files are properly configured."""

    def test_staticfiles_dirs_configured(self):
        """Verify STATICFILES_DIRS is configured."""
        from django.conf import settings

        self.assertTrue(hasattr(settings, 'STATICFILES_DIRS'))
        self.assertIn('static', [str(d.name) for d in settings.STATICFILES_DIRS])

    def test_custom_css_file_exists(self):
        """Verify custom CSS file exists."""
        from django.conf import settings

        static_path = settings.BASE_DIR / 'static' / 'css' / 'custom.css'
        self.assertTrue(static_path.exists(), f'custom.css not found at {static_path}')

    def test_code_blocks_js_file_exists(self):
        """Verify code-blocks.js file exists."""
        from django.conf import settings

        static_path = settings.BASE_DIR / 'static' / 'js' / 'code-blocks.js'
        self.assertTrue(
            static_path.exists(), f'code-blocks.js not found at {static_path}'
        )
