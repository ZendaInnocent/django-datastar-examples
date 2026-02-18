"""Tests for Recent Searches - Story 4.4"""

from pathlib import Path

import pytest

BASE_DIR = Path(__file__).parent.parent.parent


class TestRecentSearchesJavaScript:
    """Test recent searches JavaScript functionality."""

    @pytest.fixture
    def header_js_content(self):
        """Load header.js content."""
        js_path = BASE_DIR / 'static' / 'js' / 'header.js'
        return js_path.read_text(encoding='utf-8')

    def test_header_js_file_exists(self):
        """Verify header.js file exists."""
        js_path = BASE_DIR / 'static' / 'js' / 'header.js'
        assert js_path.exists(), f'header.js not found at {js_path}'

    def test_header_js_has_recent_searches_class(self, header_js_content):
        """Verify header.js contains RecentSearches class."""
        assert 'class RecentSearches' in header_js_content, (
            'Missing RecentSearches class'
        )

    def test_header_js_has_storage_key(self, header_js_content):
        """Verify recent searches uses correct storage key."""
        assert 'datastar-recent-searches' in header_js_content, (
            'Missing datastar-recent-searches storage key'
        )

    def test_header_js_has_max_items_limit(self, header_js_content):
        """Verify recent searches has max items limit."""
        assert 'maxItems' in header_js_content, 'Missing maxItems property'
        assert 'this.maxItems = 10' in header_js_content, 'Missing maxItems = 10'

    def test_header_js_has_add_method(self, header_js_content):
        """Verify RecentSearches has add method."""
        assert 'add(query, url, title)' in header_js_content, 'Missing add method'

    def test_header_js_has_remove_method(self, header_js_content):
        """Verify RecentSearches has remove method."""
        assert 'remove(query)' in header_js_content, 'Missing remove method'

    def test_header_js_has_clear_method(self, header_js_content):
        """Verify RecentSearches has clear method."""
        assert 'clear()' in header_js_content, 'Missing clear method'

    def test_header_js_has_get_all_method(self, header_js_content):
        """Verify RecentSearches has getAll method."""
        assert 'getAll()' in header_js_content, 'Missing getAll method'

    def test_header_js_handles_local_storage_unavailable(self, header_js_content):
        """Verify localStorage unavailable is handled gracefully."""
        assert 'try {' in header_js_content, 'Missing try block for localStorage'
        assert 'catch' in header_js_content, 'Missing catch block for error handling'
        assert 'localStorage not available' in header_js_content, (
            'Missing warning for unavailable localStorage'
        )

    def test_header_js_removes_duplicates_on_add(self, header_js_content):
        """Verify duplicates are removed when adding."""
        assert 'filter(' in header_js_content, 'Missing filter for removing duplicates'

    def test_header_js_trims_whitespace(self, header_js_content):
        """Verify whitespace is trimmed from queries."""
        assert '.trim()' in header_js_content, 'Missing trim() for query validation'


class TestRecentSearchesRender:
    """Test recent searches rendering functionality."""

    @pytest.fixture
    def header_js_content(self):
        """Load header.js content."""
        js_path = BASE_DIR / 'static' / 'js' / 'header.js'
        return js_path.read_text(encoding='utf-8')

    def test_header_js_has_render_function(self, header_js_content):
        """Verify renderRecentSearches function exists."""
        assert 'function renderRecentSearches' in header_js_content, (
            'Missing renderRecentSearches function'
        )

    def test_header_js_has_recent_searches_container(self, header_js_content):
        """Verify recent searches container is rendered."""
        assert "getElementById('recent-searches')" in header_js_content, (
            'Missing getElementById for recent-searches'
        )

    def test_header_js_renders_clear_all_button(self, header_js_content):
        """Verify clear all button is rendered."""
        assert 'Clear all' in header_js_content, 'Missing Clear all button'

    def test_header_js_has_run_recent_search_function(self, header_js_content):
        """Verify runRecentSearch function exists."""
        assert 'function runRecentSearch' in header_js_content, (
            'Missing runRecentSearch function'
        )

    def test_header_js_has_remove_recent_search_function(self, header_js_content):
        """Verify removeRecentSearch function exists."""
        assert 'function removeRecentSearch' in header_js_content, (
            'Missing removeRecentSearch function'
        )

    def test_header_js_has_clear_all_recent_searches_function(self, header_js_content):
        """Verify clearAllRecentSearches function exists."""
        assert 'function clearAllRecentSearches' in header_js_content, (
            'Missing clearAllRecentSearches function'
        )

    def test_header_js_has_escape_html(self, header_js_content):
        """Verify escapeHtml function exists for XSS prevention."""
        assert 'function escapeHtml' in header_js_content, 'Missing escapeHtml function'

    def test_header_js_shows_recent_on_empty_query(self, header_js_content):
        """Verify recent searches show when query is empty."""
        assert 'query || recent.length === 0' in header_js_content, (
            'Missing query/empty check'
        )


class TestRecentSearchesIntegration:
    """Integration tests for recent searches."""

    def test_base_html_has_recent_searches_container(self):
        """Verify base.html includes recent searches container."""
        html_path = BASE_DIR / 'templates' / 'base.html'
        content = html_path.read_text(encoding='utf-8')

        assert 'id="recent-searches"' in content, (
            'Missing recent-searches container in base.html'
        )

    def test_custom_css_has_recent_searches_styles(self):
        """Verify custom.css contains recent searches styles."""
        css_path = BASE_DIR / 'static' / 'css' / 'custom.css'
        content = css_path.read_text(encoding='utf-8')

        assert '.recent-searches' in content, 'Missing .recent-searches style'

    def test_custom_css_has_recent_search_item_styles(self):
        """Verify custom.css contains recent search item styles."""
        css_path = BASE_DIR / 'static' / 'css' / 'custom.css'
        content = css_path.read_text(encoding='utf-8')

        assert '.recent-search-item' in content, 'Missing .recent-search-item style'

    def test_custom_css_has_hover_state(self):
        """Verify CSS has hover state for recent search items."""
        css_path = BASE_DIR / 'static' / 'css' / 'custom.css'
        content = css_path.read_text(encoding='utf-8')

        assert '.recent-search-item:hover' in content, (
            'Missing .recent-search-item:hover state'
        )

    def test_custom_css_uses_datastar_purple(self):
        """Verify Datastar Purple is used for hover."""
        css_path = BASE_DIR / 'static' / 'css' / 'custom.css'
        content = css_path.read_text(encoding='utf-8')

        # Check for rgba version of Datastar Purple
        assert 'rgba(107, 70, 193, 0.1)' in content, (
            'Missing Datastar Purple hover color'
        )

    def test_header_js_integrates_with_search_result_click(self):
        """Verify recent searches save when result is clicked."""
        js_path = BASE_DIR / 'static' / 'js' / 'header.js'
        content = js_path.read_text(encoding='utf-8')

        # Check that click handler saves to recent searches
        assert 'saveRecentSearch' in content, 'Missing saveRecentSearch integration'

    def test_header_js_integrates_with_keyboard_navigation(self):
        """Verify recent searches save when navigating via keyboard."""
        js_path = BASE_DIR / 'static' / 'js' / 'header.js'
        content = js_path.read_text(encoding='utf-8')

        # Check navigateToSelectedResult saves recent searches
        assert 'navigateToSelectedResult' in content, 'Missing navigateToSelectedResult'
        # Should add to recent searches before navigating
        assert 'recentSearches.add' in content, 'Missing recentSearches.add call'

    def test_header_js_renders_on_modal_open(self):
        """Verify recent searches render when modal opens."""
        js_path = BASE_DIR / 'static' / 'js' / 'header.js'
        content = js_path.read_text(encoding='utf-8')

        # Check that modal shown event triggers render
        assert 'shown.bs.modal' in content, 'Missing shown.bs.modal listener'
        assert 'renderRecentSearches()' in content, (
            'Missing renderRecentSearches call on modal open'
        )


class TestRecentSearchesAcceptanceCriteria:
    """Tests verifying Acceptance Criteria from Story 4.4."""

    @pytest.fixture
    def header_js_content(self):
        """Load header.js content."""
        js_path = BASE_DIR / 'static' / 'js' / 'header.js'
        return js_path.read_text(encoding='utf-8')

    def test_ac1_recent_searches_appear_at_top(self, header_js_content):
        """AC1: Recent searches appear at top when modal opens."""
        # Verify renderRecentSearches is called on modal open
        assert 'renderRecentSearches' in header_js_content

    def test_ac2_clicking_recent_search_reruns(self, header_js_content):
        """AC2: Clicking recent search re-runs it."""
        # Verify runRecentSearch function exists and dispatches input
        assert 'runRecentSearch' in header_js_content
        assert "dispatchEvent(new Event('input'" in header_js_content

    def test_ac3_persists_across_page_reloads(self, header_js_content):
        """AC3: Recent searches persist across page reloads."""
        # Verify localStorage is used
        assert 'localStorage' in header_js_content
        assert 'localStorage.setItem' in header_js_content
        assert 'localStorage.getItem' in header_js_content

    def test_ac4_way_to_clear_recent_searches(self, header_js_content):
        """AC4: Way to clear recent searches."""
        # Verify clear all functionality
        assert 'clear()' in header_js_content
        assert 'Clear all' in header_js_content
        # Verify individual removal
        assert 'remove(' in header_js_content
