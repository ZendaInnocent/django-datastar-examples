"""
Tests for Code Tabs functionality (Story 2.3: Tab-Based Code Switching)
"""

import pytest
from django.template.loader import get_template
from django.test import Client


class TestCodeTabsTemplate:
    """Tests for code tabs template and integration."""

    def test_code_tabs_include_exists(self):
        """Verify code_tabs.html include template exists."""
        template = get_template('includes/code_tabs.html')
        assert template is not None

    def test_code_tabs_template_has_required_elements(self):
        """Verify code tabs template contains required elements."""
        template = get_template('includes/code_tabs.html')
        source = template.template.source

        # Check for tab buttons
        assert 'nav-tabs' in source
        assert 'tab-pane' in source

        # Check for HTML, Python, Response tabs
        assert 'HTML' in source
        assert 'Python' in source
        assert 'Response' in source

    def test_code_tabs_has_accessibility_attributes(self):
        """Verify code tabs have proper accessibility attributes."""
        template = get_template('includes/code_tabs.html')
        source = template.template.source

        # Check for ARIA attributes
        assert 'role="tablist"' in source
        assert 'role="tab"' in source
        assert 'role="tabpanel"' in source
        assert 'aria-selected' in source
        assert 'aria-controls' in source

    def test_code_tabs_uses_bootstrap_toggle(self):
        """Verify code tabs use Bootstrap data attributes."""
        template = get_template('includes/code_tabs.html')
        source = template.template.source

        assert 'data-bs-toggle="tab"' in source
        assert 'data-bs-target' in source


class TestCodeTabsJavaScript:
    """Tests for code tabs JavaScript functionality."""

    def test_code_tabs_js_file_exists(self):
        """Verify code-tabs.js file exists."""
        from django.conf import settings

        static_dir = settings.BASE_DIR / 'static' / 'js'
        js_file = static_dir / 'code-tabs.js'
        assert js_file.exists(), f'code-tabs.js should exist at {js_file}'

    def test_code_tabs_js_has_required_functions(self):
        """Verify code-tabs.js has required functions."""
        from django.conf import settings

        static_dir = settings.BASE_DIR / 'static' / 'js'
        js_file = static_dir / 'code-tabs.js'

        with open(js_file, encoding='utf-8') as f:
            content = f.read()

        # Check for key functions
        assert 'initCodeTabs' in content
        assert 'getActiveTab' in content
        assert 'switchToTab' in content

    def test_code_tabs_js_handles_prism_highlighting(self):
        """Verify code-tabs.js handles Prism highlighting on tab switch."""
        from django.conf import settings

        static_dir = settings.BASE_DIR / 'static' / 'js'
        js_file = static_dir / 'code-tabs.js'

        with open(js_file, encoding='utf-8') as f:
            content = f.read()

        assert 'Prism.highlightAllUnder' in content
        assert 'shown.bs.tab' in content


class TestCodeTabsCSS:
    """Tests for code tabs CSS styling."""

    def test_custom_css_has_tab_styles(self):
        """Verify custom CSS has code tabs styles."""
        from django.conf import settings

        static_dir = settings.BASE_DIR / 'static' / 'css'
        css_file = static_dir / 'custom.css'

        with open(css_file, encoding='utf-8') as f:
            content = f.read()

        # Check for tab styling
        assert '.code-tabs' in content
        assert '.code-tabs-container' in content
        assert '.tab-content' in content
        assert '.tab-pane' in content

    def test_tab_active_state_uses_datastar_purple(self):
        """Verify active tab uses Datastar Purple (#6B46C1)."""
        from django.conf import settings

        static_dir = settings.BASE_DIR / 'static' / 'css'
        css_file = static_dir / 'custom.css'

        with open(css_file, encoding='utf-8') as f:
            content = f.read()

        # Check for Datastar Purple
        assert '#6B46C1' in content
        assert '.nav-link.active' in content


@pytest.mark.django_db
class TestCodeTabsBaseTemplate:
    """Tests for base template integration."""

    def test_base_template_loads_code_tabs_js(self):
        """Verify base.html loads code-tabs.js."""
        client = Client()
        response = client.get('/')
        assert response.status_code == 200
        assert b'code-tabs.js' in response.content

    def test_base_template_loads_code_blocks_js(self):
        """Verify base.html loads code-blocks.js."""
        client = Client()
        response = client.get('/')
        assert response.status_code == 200
        assert b'code-blocks.js' in response.content


@pytest.mark.django_db
class TestCodeTabsIntegration:
    """Integration tests for code tabs functionality."""

    def test_code_tabs_include_renders(self):
        """Verify code_tabs include renders without errors."""
        from django.template import Context, Template

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
            assert 'code-tabs' in rendered
        except Exception as e:
            pytest.fail(f'Template rendering failed: {e}')
