from pathlib import Path

import pytest
from django.template.loader import get_template

BASE_DIR = Path(__file__).parent.parent.parent


class TestSearchKeyboardNavigationJavaScript:
    """Test search keyboard navigation JavaScript functionality."""

    @pytest.fixture
    def header_js_content(self):
        """Load header.js content."""
        js_path = BASE_DIR / 'static' / 'js' / 'header.js'
        return js_path.read_text(encoding='utf-8')

    def test_header_js_file_exists(self):
        """Verify header.js file exists."""
        js_path = BASE_DIR / 'static' / 'js' / 'header.js'
        assert js_path.exists(), f'header.js not found at {js_path}'

    def test_header_js_has_keyboard_navigation(self, header_js_content):
        """Verify header.js contains keyboard navigation functionality."""
        # Check for keyboard navigation functions
        assert 'searchSelectedIndex' in header_js_content, (
            'Missing searchSelectedIndex variable'
        )
        assert 'handleSearchKeyboardNavigation' in header_js_content, (
            'Missing keyboard handler'
        )
        assert 'ArrowDown' in header_js_content, 'Missing ArrowDown key handling'
        assert 'ArrowUp' in header_js_content, 'Missing ArrowUp key handling'
        assert 'Enter' in header_js_content, 'Missing Enter key handling'

    def test_header_js_prevents_default_arrow_keys(self, header_js_content):
        """Verify arrow key default behavior is prevented."""
        # Check for preventDefault on arrow keys
        assert 'event.preventDefault()' in header_js_content, (
            'Missing preventDefault for arrow keys'
        )

    def test_header_js_has_navigation_wrap_around(self, header_js_content):
        """Verify navigation wraps around at boundaries."""
        # Check for wrap-around logic
        assert 'searchSelectedIndex = 0' in header_js_content, 'Missing wrap to first'
        assert 'searchResultItems.length - 1' in header_js_content, (
            'Missing wrap to last'
        )

    def test_header_js_has_aria_selected_updates(self, header_js_content):
        """Verify aria-selected attribute is updated on selection."""
        # Check for aria-selected updates
        assert 'aria-selected' in header_js_content, (
            'Missing aria-selected attribute handling'
        )

    def test_header_js_has_result_navigation(self, header_js_content):
        """Verify result navigation on Enter key."""
        # Check for navigation to selected result
        assert 'navigateToSelectedResult' in header_js_content, (
            'Missing navigate function'
        )
        assert 'window.location.href' in header_js_content, 'Missing URL navigation'


class TestSearchKeyboardNavigationCSS:
    """Test search keyboard navigation CSS styling."""

    @pytest.fixture
    def custom_css_content(self):
        """Load custom.css content."""
        css_path = BASE_DIR / 'static' / 'css' / 'custom.css'
        return css_path.read_text(encoding='utf-8')

    def test_custom_css_has_search_result_styles(self, custom_css_content):
        """Verify custom.css contains search result styling."""
        # Check for search result item styles
        assert '.search-result-item' in custom_css_content, (
            'Missing .search-result-item style'
        )

    def test_custom_css_has_active_state(self, custom_css_content):
        """Verify CSS has .active state for keyboard selection."""
        # Check for active state
        assert '.search-result-item.active' in custom_css_content, (
            'Missing .active state for results'
        )

    def test_custom_css_has_datastar_purple_highlight(self, custom_css_content):
        """Verify Datastar Purple is used for highlighting."""
        # Check for Datastar Purple (#6B46C1)
        assert '#6B46C1' in custom_css_content, (
            'Missing Datastar Purple highlight color'
        )


class TestSearchKeyboardNavigationTemplate:
    """Test search results template accessibility attributes."""

    def test_search_results_has_role_option(self):
        """Verify result items have role='option' for accessibility."""
        template = get_template('examples/fragments/search_results.html')
        test_results = [
            {
                'title': 'Test',
                'description': 'Test desc',
                'url': '/test/',
                'type': 'example',
                'category': 'Test',
            }
        ]
        rendered = template.render({'results': test_results, 'query': 'test'})

        assert 'role="option"' in rendered, 'Missing role="option" on result items'

    def test_search_results_has_aria_selected(self):
        """Verify result items have aria-selected attribute."""
        template = get_template('examples/fragments/search_results.html')
        test_results = [
            {
                'title': 'Test',
                'description': 'Test desc',
                'url': '/test/',
                'type': 'example',
                'category': 'Test',
            }
        ]
        rendered = template.render({'results': test_results, 'query': 'test'})

        assert 'aria-selected' in rendered, 'Missing aria-selected attribute'

    def test_search_results_has_listbox_role(self):
        """Verify results container has role='listbox'."""
        template = get_template('examples/fragments/search_results.html')
        test_results = [
            {
                'title': 'Test',
                'description': 'Test desc',
                'url': '/test/',
                'type': 'example',
                'category': 'Test',
            }
        ]
        rendered = template.render({'results': test_results, 'query': 'test'})

        assert 'role="listbox"' in rendered, 'Missing role="listbox" on container'

    def test_search_results_has_data_result_url(self):
        """Verify result items have data-result-url for keyboard navigation."""
        template = get_template('examples/fragments/search_results.html')
        test_results = [
            {
                'title': 'Test',
                'description': 'Test desc',
                'url': '/test/',
                'type': 'example',
                'category': 'Test',
            }
        ]
        rendered = template.render({'results': test_results, 'query': 'test'})

        assert 'data-result-url' in rendered, 'Missing data-result-url attribute'


class TestSearchKeyboardNavigationIntegration:
    """Integration tests for search keyboard navigation."""

    def test_search_modal_template_has_results_container(self):
        """Verify base.html includes search results container."""
        html_path = BASE_DIR / 'templates' / 'base.html'
        content = html_path.read_text(encoding='utf-8')

        assert 'id="search-results"' in content, 'Missing search-results container'
        assert 'id="search-modal"' in content, 'Missing search-modal element'

    def test_search_modal_has_keyboard_hint_footer(self):
        """Verify modal footer shows keyboard shortcuts."""
        html_path = BASE_DIR / 'templates' / 'base.html'
        content = html_path.read_text(encoding='utf-8')

        # Check for keyboard hints in footer
        assert '↑' in content, 'Missing arrow key hint'
        assert '↓' in content, 'Missing arrow key hint'
        assert 'Enter' in content, 'Missing Enter key hint'
        assert 'Esc' in content, 'Missing Escape key hint'

    def test_header_js_resets_selection_on_new_search(self):
        """Verify selection resets when new search is performed."""
        js_path = BASE_DIR / 'static' / 'js' / 'header.js'
        content = js_path.read_text(encoding='utf-8')

        # Check for reset on input event
        assert 'resetSearchSelection' in content, 'Missing reset function'
        assert "searchInput.addEventListener('input'" in content, (
            'Missing input listener for reset'
        )

    def test_header_js_uses_mutation_observer(self):
        """Verify MutationObserver is used to detect results changes."""
        js_path = BASE_DIR / 'static' / 'js' / 'header.js'
        content = js_path.read_text(encoding='utf-8')

        assert 'MutationObserver' in content, (
            'Missing MutationObserver for dynamic results'
        )
