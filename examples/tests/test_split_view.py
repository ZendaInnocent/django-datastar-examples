"""Tests for Split View functionality - Story 2.4"""

from pathlib import Path

from django.test import TestCase
from django.template import TemplateDoesNotExist
from django.template.loader import get_template


class SplitViewTemplateTests(TestCase):
    """Test split view template include exists and renders."""

    def test_split_view_include_exists(self):
        """Verify split_view.html include template exists."""
        template_path = Path('includes/split_view.html')
        # Check file exists in templates directory
        base_dir = Path(__file__).parent.parent.parent
        full_path = base_dir / 'templates' / template_path
        self.assertTrue(
            full_path.exists(), f'Split view template not found at {full_path}'
        )

    def test_split_view_include_renders(self):
        """Verify split_view include renders without errors."""
        try:
            template = get_template('includes/split_view.html')
            # Render with empty context - should not raise
            rendered = template.render({})
            # Check for key elements (use simple substring matching)
            self.assertIn('split-view-container', rendered)
            self.assertIn('split-view-code', rendered)
            self.assertIn('split-view-demo', rendered)
            self.assertIn('split-divider', rendered)
            self.assertIn('data-split-view', rendered)
        except TemplateDoesNotExist:
            self.fail('split_view.html template does not exist')


class SplitViewJavaScriptTests(TestCase):
    """Test split view JavaScript file."""

    def test_split_view_js_file_exists(self):
        """Verify split-view.js file exists."""
        base_dir = Path(__file__).parent.parent.parent
        js_path = base_dir / 'static' / 'js' / 'split-view.js'
        self.assertTrue(js_path.exists(), f'split-view.js not found at {js_path}')

    def test_split_view_js_has_drag_functionality(self):
        """Verify split-view.js contains draggable divider functionality."""
        base_dir = Path(__file__).parent.parent.parent
        js_path = base_dir / 'static' / 'js' / 'split-view.js'

        with open(js_path) as f:
            content = f.read()

        # Check for key functionality
        self.assertIn('mousedown', content, 'Missing mousedown event handler')
        self.assertIn('mousemove', content, 'Missing mousemove event handler')
        self.assertIn('mouseup', content, 'Missing mouseup event handler')
        self.assertIn(
            'localStorage', content, 'Missing localStorage for preference persistence'
        )
        self.assertIn(
            'split-view-ratio', content, 'Missing split-view-ratio localStorage key'
        )

    def test_split_view_js_has_mobile_tabs(self):
        """Verify split-view.js contains mobile tab switching functionality."""
        base_dir = Path(__file__).parent.parent.parent
        js_path = base_dir / 'static' / 'js' / 'split-view.js'

        with open(js_path) as f:
            content = f.read()

        # Check for mobile functionality
        self.assertIn('mobile', content.lower(), 'Missing mobile functionality')
        self.assertIn('resize', content, 'Missing resize handler')

    def test_split_view_js_has_keyboard_accessibility(self):
        """Verify split-view.js has keyboard accessibility."""
        base_dir = Path(__file__).parent.parent.parent
        js_path = base_dir / 'static' / 'js' / 'split-view.js'

        with open(js_path) as f:
            content = f.read()

        self.assertIn('keydown', content, 'Missing keyboard event handler')
        self.assertIn('ArrowLeft', content, 'Missing ArrowLeft key support')
        self.assertIn('ArrowRight', content, 'Missing ArrowRight key support')


class SplitViewCSSTests(TestCase):
    """Test split view CSS styles."""

    def test_custom_css_has_split_view_styles(self):
        """Verify custom CSS contains split view styles."""
        base_dir = Path(__file__).parent.parent.parent
        css_path = base_dir / 'static' / 'css' / 'custom.css'

        with open(css_path) as f:
            content = f.read()

        # Check for key CSS classes
        self.assertIn('.split-view-container', content, 'Missing .split-view-container')
        self.assertIn('.split-view-code', content, 'Missing .split-view-code')
        self.assertIn('.split-view-demo', content, 'Missing .split-view-demo')
        self.assertIn('.split-view-divider', content, 'Missing .split-view-divider')

    def test_split_view_uses_flexbox(self):
        """Verify split view uses flexbox layout."""
        base_dir = Path(__file__).parent.parent.parent
        css_path = base_dir / 'static' / 'css' / 'custom.css'

        with open(css_path) as f:
            content = f.read()

        self.assertIn('display: flex', content, 'Split view should use flexbox')

    def test_split_view_has_responsive_breakpoint(self):
        """Verify split view has responsive breakpoint at 1024px."""
        base_dir = Path(__file__).parent.parent.parent
        css_path = base_dir / 'static' / 'css' / 'custom.css'

        with open(css_path) as f:
            content = f.read()

        self.assertIn('1023px', content, 'Missing responsive breakpoint at 1023px')

    def test_split_view_divider_uses_datastar_purple(self):
        """Verify divider hover uses Datastar Purple (#6B46C1)."""
        base_dir = Path(__file__).parent.parent.parent
        css_path = base_dir / 'static' / 'css' / 'custom.css'

        with open(css_path) as f:
            content = f.read()

        self.assertIn(
            '#6B46C1', content, 'Divider should use Datastar Purple (#6B46C1)'
        )

    def test_split_view_has_mobile_view_tabs(self):
        """Verify split view has mobile view tabs styles."""
        base_dir = Path(__file__).parent.parent.parent
        css_path = base_dir / 'static' / 'css' / 'custom.css'

        with open(css_path) as f:
            content = f.read()

        self.assertIn('.mobile-view-tabs', content, 'Missing .mobile-view-tabs styles')


class SplitViewBaseTemplateTests(TestCase):
    """Test split view integration with base template."""

    def test_base_template_loads_split_view_js(self):
        """Verify base.html loads split-view.js."""
        base_dir = Path(__file__).parent.parent.parent
        template_path = base_dir / 'templates' / 'base.html'

        with open(template_path) as f:
            content = f.read()

        self.assertIn('split-view.js', content, 'base.html should load split-view.js')


class SplitViewIntegrationTests(TestCase):
    """Integration tests for split view functionality."""

    def test_split_view_reuses_code_tabs(self):
        """Verify split view reuses code_tabs include from Story 2.3."""
        base_dir = Path(__file__).parent.parent.parent
        split_view_path = base_dir / 'templates' / 'includes' / 'split_view.html'

        with open(split_view_path) as f:
            content = f.read()

        self.assertIn(
            'includes/code_tabs.html',
            content,
            'Split view should include code_tabs.html from Story 2.3',
        )

    def test_split_view_has_accessible_divider(self):
        """Verify divider has accessibility attributes."""
        base_dir = Path(__file__).parent.parent.parent
        split_view_path = base_dir / 'templates' / 'includes' / 'split_view.html'

        with open(split_view_path) as f:
            content = f.read()

        self.assertIn(
            'role="separator"', content, "Divider should have role='separator'"
        )
        self.assertIn(
            'aria-orientation', content, 'Divider should have aria-orientation'
        )
        self.assertIn('tabindex="0"', content, 'Divider should be keyboard focusable')

    def test_split_view_has_mobile_view_tabs_html(self):
        """Verify split_view.html includes mobile view tabs HTML structure."""
        base_dir = Path(__file__).parent.parent.parent
        split_view_path = base_dir / 'templates' / 'includes' / 'split_view.html'

        with open(split_view_path) as f:
            content = f.read()

        self.assertIn(
            'mobile-view-tabs', content, 'Split view should have mobile view tabs HTML'
        )
        self.assertIn('tab-mobile-demo', content, 'Mobile demo tab should exist')
        self.assertIn('tab-mobile-code', content, 'Mobile code tab should exist')


class SplitViewExampleIntegrationTests(TestCase):
    """Test split view is integrated into example templates."""

    def test_active_search_uses_split_view(self):
        """Verify active_search.html uses split_view include."""
        base_dir = Path(__file__).parent.parent.parent
        template_path = (
            base_dir / 'examples' / 'templates' / 'examples' / 'active_search.html'
        )

        with open(template_path) as f:
            content = f.read()

        self.assertIn(
            "include 'includes/split_view.html'",
            content,
            'active_search.html should include split_view.html',
        )

    def test_split_view_js_has_touch_events(self):
        """Verify split-view.js has touch event handlers."""
        base_dir = Path(__file__).parent.parent.parent
        js_path = base_dir / 'static' / 'js' / 'split-view.js'

        with open(js_path) as f:
            content = f.read()

        self.assertIn('touchstart', content, 'split-view.js should have touchstart')
        self.assertIn('touchmove', content, 'split-view.js should have touchmove')
        self.assertIn('touchend', content, 'split-view.js should have touchend')
