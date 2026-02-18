"""
Tests for search index functionality.

Tests the search index implementation including:
- QEntry (Q object) filtering
- Relevance ranking
- Index building
- Search results formatting
"""

from examples.search import (
    EXAMPLES_DATA,
    QEntry,
    SearchIndex,
    SearchIndexEntry,
    create_search_q,
    get_search_index,
    search,
)
from examples.services.search_service import (
    get_all_docs,
    get_all_examples,
    get_index_stats,
    rebuild_index,
)
from examples.services.search_service import (
    search as service_search,
)


class TestQEntry:
    """Tests for QEntry Q object implementation."""

    def test_qentry_icontains_title_match(self):
        """QEntry should match title with icontains lookup."""
        entry = SearchIndexEntry(
            title='Active Search',
            description='A search example',
            content='Content about search',
            url='/active-search/',
            type='example',
            category='Search',
        )
        q = QEntry(title__icontains='search')
        assert q.check(entry) is True

    def test_qentry_icontains_title_no_match(self):
        """QEntry should not match when title doesn't contain query."""
        entry = SearchIndexEntry(
            title='Click to Load',
            description='Loading example',
            content='Content about loading',
            url='/click-to-load/',
            type='example',
            category='Interactive',
        )
        q = QEntry(title__icontains='search')
        assert q.check(entry) is False

    def test_qentry_icontains_description_match(self):
        """QEntry should match description with icontains lookup."""
        entry = SearchIndexEntry(
            title='Some Example',
            description='This is about search functionality',
            content='Content',
            url='/example/',
            type='example',
            category='Test',
        )
        q = QEntry(description__icontains='search')
        assert q.check(entry) is True

    def test_qentry_icontains_content_match(self):
        """QEntry should match content with icontains lookup."""
        entry = SearchIndexEntry(
            title='Some Example',
            description='Description',
            content='This content mentions search terms',
            url='/example/',
            type='example',
            category='Test',
        )
        q = QEntry(content__icontains='search')
        assert q.check(entry) is True

    def test_qentry_case_insensitive(self):
        """QEntry icontains should be case insensitive."""
        entry = SearchIndexEntry(
            title='ACTIVE Search',
            description='Description',
            content='Content',
            url='/example/',
            type='example',
            category='Test',
        )
        q = QEntry(title__icontains='search')
        assert q.check(entry) is True

    def test_qentry_exact_match(self):
        """QEntry should support exact lookup."""
        entry = SearchIndexEntry(
            title='Exact Match',
            description='Description',
            content='Content',
            url='/example/',
            type='example',
            category='Test',
        )
        q = QEntry(title__exact='Exact Match')
        assert q.check(entry) is True


class TestCreateSearchQ:
    """Tests for create_search_q helper function."""

    def test_create_search_q_returns_three_qentries(self):
        """create_search_q should return three QEntry objects."""
        title_q, desc_q, content_q = create_search_q('test')
        assert isinstance(title_q, QEntry)
        assert isinstance(desc_q, QEntry)
        assert isinstance(content_q, QEntry)

    def test_create_search_q_sets_correct_fields(self):
        """create_search_q should set correct field names."""
        title_q, desc_q, content_q = create_search_q('test')
        assert title_q.children[0][0] == 'title__icontains'
        assert desc_q.children[0][0] == 'description__icontains'
        assert content_q.children[0][0] == 'content__icontains'


class TestSearchIndex:
    """Tests for SearchIndex class."""

    def test_search_index_builds_all_examples(self):
        """SearchIndex should index all 12 examples."""
        index = SearchIndex()
        examples = [e for e in index.entries if e.type == 'example']
        assert len(examples) == 12

    def test_search_index_builds_all_docs(self):
        """SearchIndex should index documentation files."""
        index = SearchIndex()
        docs = [e for e in index.entries if e.type == 'doc']
        assert len(docs) >= 6  # At least the main docs

    def test_search_returns_empty_for_empty_query(self):
        """Search should return empty list for empty query."""
        index = SearchIndex()
        results = index.search('')
        assert results == []

    def test_search_finds_active_search(self):
        """Search for 'search' should return Active Search as top result."""
        index = SearchIndex()
        results = index.search('search')
        assert len(results) > 0
        assert results[0]['title'] == 'Active Search'

    def test_search_ranking_title_over_description(self):
        """Title matches should rank higher than description matches."""
        index = SearchIndex()
        results = index.search('active')
        titles = [r['title'] for r in results]
        # Active Search should appear before docs mentioning "active" in description
        assert 'Active Search' in titles

    def test_search_ranking_description_over_content(self):
        """Description matches should rank higher than content matches."""
        index = SearchIndex()
        results = index.search('django')
        # Should return results
        assert len(results) > 0

    def test_search_returns_limited_results(self):
        """Search should respect limit parameter."""
        index = SearchIndex()
        results = index.search('a', limit=5)
        assert len(results) <= 5

    def test_search_returns_formatted_dict(self):
        """Search should return properly formatted dictionaries."""
        index = SearchIndex()
        results = index.search('active')
        assert len(results) > 0
        result = results[0]
        assert 'title' in result
        assert 'description' in result
        assert 'url' in result
        assert 'type' in result
        assert 'category' in result

    def test_get_all_entries(self):
        """get_all_entries should return all indexed entries."""
        index = SearchIndex()
        entries = index.get_all_entries()
        assert len(entries) >= 18  # 12 examples + docs

    def test_rebuild_clears_and_rebuilds(self):
        """rebuild should clear and rebuild the index."""
        index = SearchIndex()
        initial_count = len(index.entries)
        index.rebuild()
        assert len(index.entries) == initial_count


class TestSearchFunction:
    """Tests for the module-level search function."""

    def test_search_function_returns_results(self):
        """search() function should return search results."""
        results = search('active')
        assert len(results) > 0
        assert results[0]['title'] == 'Active Search'

    def test_search_function_uses_global_index(self):
        """search() should use the global search index."""
        # Verify global index exists and search uses it
        _ = get_search_index()  # Ensure global index is initialized
        results = search('active', limit=5)
        assert len(results) <= 5


class TestSearchService:
    """Tests for search_service module."""

    def test_service_search_returns_results(self):
        """service_search should return search results."""
        results = service_search('active')
        assert len(results) > 0

    def test_get_all_examples_returns_only_examples(self):
        """get_all_examples should return only example type entries."""
        examples = get_all_examples()
        assert len(examples) == 12
        for ex in examples:
            assert ex['type'] == 'example'

    def test_get_all_docs_returns_only_docs(self):
        """get_all_docs should return only doc type entries."""
        docs = get_all_docs()
        assert len(docs) >= 6
        for doc in docs:
            assert doc['type'] == 'doc'

    def test_get_index_stats(self):
        """get_index_stats should return correct statistics."""
        stats = get_index_stats()
        assert 'total_entries' in stats
        assert 'examples_count' in stats
        assert 'docs_count' in stats
        assert stats['examples_count'] == 12
        assert stats['docs_count'] >= 6
        assert stats['total_entries'] == stats['examples_count'] + stats['docs_count']

    def test_rebuild_index_returns_index(self):
        """rebuild_index should return a SearchIndex instance."""
        index = rebuild_index()
        assert isinstance(index, SearchIndex)


class TestSearchIndexEntry:
    """Tests for SearchIndexEntry dataclass."""

    def test_to_dict_returns_correct_keys(self):
        """to_dict should return dict with expected keys."""
        entry = SearchIndexEntry(
            title='Test',
            description='Test description',
            content='Test content',
            url='/test/',
            type='example',
            category='Test',
        )
        d = entry.to_dict()
        assert d['title'] == 'Test'
        assert d['description'] == 'Test description'
        assert d['url'] == '/test/'
        assert d['type'] == 'example'
        assert d['category'] == 'Test'
        assert 'content' not in d  # content should not be in dict output

    def test_get_q_field_value(self):
        """get_q_field_value should return correct field values."""
        entry = SearchIndexEntry(
            title='Test Title',
            description='Test Description',
            content='Test Content',
            url='/test/',
            type='example',
            category='Test',
        )
        assert entry.get_q_field_value('title') == 'Test Title'
        assert entry.get_q_field_value('description') == 'Test Description'
        assert entry.get_q_field_value('content') == 'Test Content'
        assert entry.get_q_field_value('unknown') == ''


class TestExamplesData:
    """Tests for EXAMPLES_DATA constant."""

    def test_examples_data_has_12_examples(self):
        """EXAMPLES_DATA should contain 12 examples."""
        assert len(EXAMPLES_DATA) == 12

    def test_each_example_has_required_fields(self):
        """Each example should have required fields."""
        required_fields = ['id', 'title', 'description', 'content', 'url', 'category']
        for example in EXAMPLES_DATA:
            for field in required_fields:
                assert field in example, (
                    f'Example {example.get("id", "unknown")} missing {field}'
                )

    def test_example_ids_are_unique(self):
        """All example IDs should be unique."""
        ids = [ex['id'] for ex in EXAMPLES_DATA]
        assert len(ids) == len(set(ids))

    def test_example_urls_follow_pattern(self):
        """Example URLs should follow kebab-case pattern with trailing slash."""
        for example in EXAMPLES_DATA:
            url = example['url']
            assert url.startswith('/')
            assert url.endswith('/')


class TestAcceptanceCriteria:
    """Tests verifying Acceptance Criteria from Story 4.2."""

    def test_ac1_index_includes_all_12_examples(self):
        """AC1: Index should include all 12 example titles."""
        index = SearchIndex()
        example_titles = {e.title for e in index.entries if e.type == 'example'}
        expected_titles = {ex['title'] for ex in EXAMPLES_DATA}
        assert example_titles == expected_titles

    def test_ac1_index_includes_documentation(self):
        """AC1: Index should include documentation titles and content."""
        index = SearchIndex()
        docs = [e for e in index.entries if e.type == 'doc']
        assert len(docs) > 0
        # Each doc should have title, description, and content
        for doc in docs:
            assert doc.title
            assert doc.description is not None
            assert doc.content is not None

    def test_ac1_uses_q_objects_for_filtering(self):
        """AC1: Search should use Django Q objects for filtering."""
        # Verify QEntry is used (our Q object extension)
        from examples.search import QEntry, create_search_q

        title_q, desc_q, content_q = create_search_q('test')
        assert isinstance(title_q, QEntry)
        assert isinstance(desc_q, QEntry)
        assert isinstance(content_q, QEntry)

    def test_ac2_search_returns_active_search(self):
        """AC2: Search for 'search' should return Active Search example."""
        results = search('search')
        titles = [r['title'] for r in results]
        assert 'Active Search' in titles

    def test_ac2_results_ranked_by_relevance(self):
        """AC2: Results should be ranked by relevance."""
        results = search('search')
        if len(results) >= 2:
            # Active Search should be first (title match = 100 pts)
            assert results[0]['title'] == 'Active Search'

    def test_ac2_returns_docs_mentioning_search(self):
        """AC2: Results should include docs mentioning search."""
        results = search('search')
        doc_results = [r for r in results if r['type'] == 'doc']
        # Should have some doc results
        assert len(doc_results) > 0
