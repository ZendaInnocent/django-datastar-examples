"""
Tests for Code Tabs functionality (Story 2.3: Tab-Based Code Switching)
"""

from django.test import TestCase, Client
from django.urls import reverse


class CodeTabsTemplateTests(TestCase):
    """Tests for code tabs template and integration."""

    def setUp(self):
        self.client = Client()

    def test_code_tabs_include_exists(self):
        """Verify code_tabs.html include template exists."""
        from django.template.loader import get_template

        template = get_template('includes/code_tabs.html')
        self.assertTrue(template is not None)

    def test_code_tabs_template_has_required_elements(self):
        """Verify code tabs template contains required elements."""
        from django.template.loader import get_template

        template = get_template('includes/code_tabs.html')
        source = template.template.source

        # Check for tab buttons
        self.assertIn('nav-tabs', source)
        self.assertIn('tab-pane', source)

        # Check for HTML, Python, Response tabs
        self.assertIn('HTML', source)
        self.assertIn('Python', source)
        self.assertIn('Response', source)

    def test_code_tabs_has_accessibility_attributes(self):
        """Verify code tabs have proper accessibility attributes."""
        from django.template.loader import get_template

        template = get_template('includes/code_tabs.html')
        source = template.template.source

        # Check for ARIA attributes
        self.assertIn('role="tablist"', source)
        self.assertIn('role="tab"', source)
        self.assertIn('role="tabpanel"', source)
        self.assertIn('aria-selected', source)
        self.assertIn('aria-controls', source)

    def test_code_tabs_uses_bootstrap_toggle(self):
        """Verify code tabs use Bootstrap data attributes."""
        from django.template.loader import get_template

        template = get_template('includes/code_tabs.html')
        source = template.template.source

        self.assertIn('data-bs-toggle="tab"', source)
        self.assertIn('data-bs-target', source)


class CodeTabsJavaScriptTests(TestCase):
    """Tests for code tabs JavaScript functionality."""

    def test_code_tabs_js_file_exists(self):
        """Verify code-tabs.js file exists."""
        from django.conf import settings

        static_dir = settings.BASE_DIR / 'static' / 'js'
        js_file = static_dir / 'code-tabs.js'
        self.assertTrue(js_file.exists(), f'code-tabs.js should exist at {js_file}')

    def test_code_tabs_js_has_required_functions(self):
        """Verify code-tabs.js has required functions."""
        from django.conf import settings

        static_dir = settings.BASE_DIR / 'static' / 'js'
        js_file = static_dir / 'code-tabs.js'

        with open(js_file, encoding='utf-8') as f:
            content = f.read()

        # Check for key functions
        self.assertIn('initCodeTabs', content)
        self.assertIn('getActiveTab', content)
        self.assertIn('switchToTab', content)

    def test_code_tabs_js_handles_prism_highlighting(self):
        """Verify code-tabs.js handles Prism highlighting on tab switch."""
        from django.conf import settings

        static_dir = settings.BASE_DIR / 'static' / 'js'
        js_file = static_dir / 'code-tabs.js'

        with open(js_file, encoding='utf-8') as f:
            content = f.read()

        self.assertIn('Prism.highlightAllUnder', content)
        self.assertIn('shown.bs.tab', content)


class CodeTabsCSSTests(TestCase):
    """Tests for code tabs CSS styling."""

    def test_custom_css_has_tab_styles(self):
        """Verify custom CSS has code tabs styles."""
        from django.conf import settings

        static_dir = settings.BASE_DIR / 'static' / 'css'
        css_file = static_dir / 'custom.css'

        with open(css_file, encoding='utf-8') as f:
            content = f.read()

        # Check for tab styling
        self.assertIn('.code-tabs', content)
        self.assertIn('.code-tabs-container', content)
        self.assertIn('.tab-content', content)
        self.assertIn('.tab-pane', content)

    def test_tab_active_state_uses_datastar_purple(self):
        """Verify active tab uses Datastar Purple (#6B46C1)."""
        from django.conf import settings

        static_dir = settings.BASE_DIR / 'static' / 'css'
        css_file = static_dir / 'custom.css'

        with open(css_file, encoding='utf-8') as f:
            content = f.read()

        # Check for Datastar Purple
        self.assertIn('#6B46C1', content)
        self.assertIn('.nav-link.active', content)


class CodeTabsBaseTemplateTests(TestCase):
    """Tests for base template integration."""

    def setUp(self):
        self.client = Client()

    def test_base_template_loads_code_tabs_js(self):
        """Verify base.html loads code-tabs.js."""
        response = self.client.get(reverse('examples:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'code-tabs.js', response.content)

    def test_base_template_loads_code_blocks_js(self):
        """Verify base.html loads code-blocks.js."""
        response = self.client.get(reverse('examples:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'code-blocks.js', response.content)


class CodeTabsIntegrationTests(TestCase):
    """Integration tests for code tabs functionality."""

    def setUp(self):
        self.client = Client()

    def test_code_tabs_include_renders(self):
        """Verify code_tabs include renders without errors."""
        from django.template import Template, Context

        template = Template(
            '{% load static %}'
            '{% include "includes/code_tabs.html" with '
            'html_code="<div>test</div>" '
            'python_code="print(\'hello\')" '
            'response_code=\'{"key": "value"}\' %}'
        )

        # Should render without errors
        try:
            rendered = template.render(Context({}))
            self.assertIn('code-tabs', rendered)
        except Exception as e:
            self.fail(f'Template rendering failed: {e}')
