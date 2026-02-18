"""Tests for Split View functionality - Story 2.4"""

from pathlib import Path

import pytest
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

BASE_DIR = Path(__file__).parent.parent.parent


class TestSplitViewTemplate:
    """Test split view template include exists and renders."""

    def test_split_view_include_exists(self):
        """Verify split_view.html include template exists."""
        template_path = BASE_DIR / 'templates' / 'includes' / 'split_view.html'
        assert template_path.exists(), (
            f'Split view template not found at {template_path}'
        )

    def test_split_view_include_renders(self):
        """Verify split_view include renders without errors."""
        try:
            template = get_template('includes/split_view.html')
            # Render with empty context - should not raise
            rendered = template.render({})
            # Check for key elements (use simple substring matching)
            assert 'split-view-container' in rendered
            assert 'split-view-code' in rendered
            assert 'split-view-demo' in rendered
            assert 'split-divider' in rendered
            assert 'data-split-view' in rendered
        except TemplateDoesNotExist:
            pytest.fail('split_view.html template does not exist')


class TestSplitViewJavaScript:
    """Test split view JavaScript file."""

    @pytest.fixture
    def split_view_js_content(self):
        """Load split-view.js content."""
        js_path = BASE_DIR / 'static' / 'js' / 'split-view.js'
        return js_path.read_text(encoding='utf-8')

    def test_split_view_js_file_exists(self):
        """Verify split-view.js file exists."""
        js_path = BASE_DIR / 'static' / 'js' / 'split-view.js'
        assert js_path.exists(), f'split-view.js not found at {js_path}'

    def test_split_view_js_has_drag_functionality(self, split_view_js_content):
        """Verify split-view.js contains draggable divider functionality."""
        # Check for key functionality
        assert 'mousedown' in split_view_js_content, 'Missing mousedown event handler'
        assert 'mousemove' in split_view_js_content, 'Missing mousemove event handler'
        assert 'mouseup' in split_view_js_content, 'Missing mouseup event handler'
        assert 'localStorage' in split_view_js_content, (
            'Missing localStorage for preference persistence'
        )
        assert 'split-view-ratio' in split_view_js_content, (
            'Missing split-view-ratio localStorage key'
        )

    def test_split_view_js_has_mobile_tabs(self, split_view_js_content):
        """Verify split-view.js contains mobile tab switching functionality."""
        # Check for mobile functionality
        assert 'mobile' in split_view_js_content.lower(), 'Missing mobile functionality'
        assert 'resize' in split_view_js_content, 'Missing resize handler'

    def test_split_view_js_has_keyboard_accessibility(self, split_view_js_content):
        """Verify split-view.js has keyboard accessibility."""
        assert 'keydown' in split_view_js_content, 'Missing keyboard event handler'
        assert 'ArrowLeft' in split_view_js_content, 'Missing ArrowLeft key support'
        assert 'ArrowRight' in split_view_js_content, 'Missing ArrowRight key support'


class TestSplitViewCSS:
    """Test split view CSS styles."""

    @pytest.fixture
    def custom_css_content(self):
        """Load custom.css content."""
        css_path = BASE_DIR / 'static' / 'css' / 'custom.css'
        return css_path.read_text(encoding='utf-8')

    def test_custom_css_has_split_view_styles(self, custom_css_content):
        """Verify custom CSS contains split view styles."""
        # Check for key CSS classes
        assert '.split-view-container' in custom_css_content, (
            'Missing .split-view-container'
        )
        assert '.split-view-code' in custom_css_content, 'Missing .split-view-code'
        assert '.split-view-demo' in custom_css_content, 'Missing .split-view-demo'
        assert '.split-view-divider' in custom_css_content, (
            'Missing .split-view-divider'
        )

    def test_split_view_uses_flexbox(self, custom_css_content):
        """Verify split view uses flexbox layout."""
        assert 'display: flex' in custom_css_content, 'Split view should use flexbox'

    def test_split_view_has_responsive_breakpoint(self, custom_css_content):
        """Verify split view has responsive breakpoint at 1024px."""
        assert '1023px' in custom_css_content, 'Missing responsive breakpoint at 1023px'

    def test_split_view_divider_uses_datastar_purple(self, custom_css_content):
        """Verify divider hover uses Datastar Purple (#6B46C1)."""
        assert '#6B46C1' in custom_css_content, (
            'Divider should use Datastar Purple (#6B46C1)'
        )

    def test_split_view_has_mobile_view_tabs(self, custom_css_content):
        """Verify split view has mobile view tabs styles."""
        assert '.mobile-view-tabs' in custom_css_content, (
            'Missing .mobile-view-tabs styles'
        )


class TestSplitViewBaseTemplate:
    """Test split view integration with base template."""

    def test_base_template_loads_split_view_js(self):
        """Verify base.html loads split-view.js."""
        template_path = BASE_DIR / 'templates' / 'base.html'
        content = template_path.read_text(encoding='utf-8')

        assert 'split-view.js' in content, 'base.html should load split-view.js'


class TestSplitViewIntegration:
    """Integration tests for split view functionality."""

    def test_split_view_reuses_code_tabs(self):
        """Verify split view reuses code_tabs include from Story 2.3."""
        split_view_path = BASE_DIR / 'templates' / 'includes' / 'split_view.html'
        content = split_view_path.read_text(encoding='utf-8')

        assert 'includes/code_tabs.html' in content, (
            'Split view should include code_tabs.html from Story 2.3'
        )

    def test_split_view_has_accessible_divider(self):
        """Verify divider has accessibility attributes."""
        split_view_path = BASE_DIR / 'templates' / 'includes' / 'split_view.html'
        content = split_view_path.read_text(encoding='utf-8')

        assert 'role="separator"' in content, "Divider should have role='separator'"
        assert 'aria-orientation' in content, 'Divider should have aria-orientation'
        assert 'tabindex="0"' in content, 'Divider should be keyboard focusable'

    def test_split_view_has_mobile_view_tabs_html(self):
        """Verify split_view.html includes mobile view tabs HTML structure."""
        split_view_path = BASE_DIR / 'templates' / 'includes' / 'split_view.html'
        content = split_view_path.read_text(encoding='utf-8')

        assert 'mobile-view-tabs' in content, (
            'Split view should have mobile view tabs HTML'
        )
        assert 'tab-mobile-demo' in content, 'Mobile demo tab should exist'
        assert 'tab-mobile-code' in content, 'Mobile code tab should exist'


class TestSplitViewExampleIntegration:
    """Test split view is integrated into example templates."""

    def test_active_search_uses_split_view(self):
        """Verify active_search.html uses split_view include."""
        template_path = (
            BASE_DIR / 'examples' / 'templates' / 'examples' / 'active_search.html'
        )
        content = template_path.read_text(encoding='utf-8')

        assert "include 'includes/split_view.html'" in content, (
            'active_search.html should include split_view.html'
        )

    def test_split_view_js_has_touch_events(self):
        """Verify split-view.js has touch event handlers."""
        js_path = BASE_DIR / 'static' / 'js' / 'split-view.js'
        content = js_path.read_text(encoding='utf-8')

        assert 'touchstart' in content, 'split-view.js should have touchstart'
        assert 'touchmove' in content, 'split-view.js should have touchmove'
        assert 'touchend' in content, 'split-view.js should have touchend'
