"""
Tests for howto_config module.

Tests HowTo configuration including:
- Example configurations
- HowTo step generation
- Doc links
- URL patterns
"""

import pytest

from examples.howto_config import (
    EXAMPLES,
    get_example,
    get_all_examples,
    extract_view_code,
    get_url_pattern,
    HowToExample,
    HowToStep,
)
from examples import views


@pytest.mark.django_db
class TestHowToExamples:
    """Tests for HowTo example configurations."""

    def test_examples_dict_exists(self):
        """EXAMPLES dictionary exists."""
        assert isinstance(EXAMPLES, dict)

    def test_has_13_examples(self):
        """EXAMPLES has 13 examples (12 examples + system-messages)."""
        assert len(EXAMPLES) == 13

    def test_all_examples_have_slugs(self):
        """All examples have slug field."""
        for slug, example in EXAMPLES.items():
            assert isinstance(example, HowToExample)
            assert example.slug == slug

    def test_all_examples_have_titles(self):
        """All examples have title field."""
        for example in EXAMPLES.values():
            assert isinstance(example, HowToExample)
            assert example.title is not None
            assert len(example.title) > 0

    def test_all_examples_have_descriptions(self):
        """All examples have description field."""
        for example in EXAMPLES.values():
            assert isinstance(example, HowToExample)
            assert example.description is not None

    def test_all_examples_have_steps(self):
        """All examples have steps list."""
        for example in EXAMPLES.values():
            assert isinstance(example, HowToExample)
            assert isinstance(example.steps, list)

    def test_all_examples_have_doc_links(self):
        """All examples have doc_links list."""
        for example in EXAMPLES.values():
            assert isinstance(example, HowToExample)
            assert isinstance(example.doc_links, list)

    def test_example_slugs_match_expected(self):
        """Example slugs match expected set."""
        expected_slugs = {
            'active-search',
            'click-to-load',
            'edit-row',
            'delete-row',
            'todo-mvc',
            'inline-validation',
            'infinite-scroll',
            'lazy-tabs',
            'file-upload',
            'sortable',
            'notifications',
            'bulk-update',
            'system-messages',
        }
        assert set(EXAMPLES.keys()) == expected_slugs


@pytest.mark.django_db
class TestGetExample:
    """Tests for get_example function."""

    def test_get_example_returns_example(self):
        """get_example returns HowToExample."""
        example = get_example('active-search')
        assert isinstance(example, HowToExample)

    def test_get_example_with_valid_slug(self):
        """get_example works with valid slug."""
        example = get_example('todo-mvc')
        assert example is not None
        assert example.title == 'TodoMVC'

    def test_get_example_with_invalid_slug(self):
        """get_example returns None for invalid slug."""
        example = get_example('nonexistent')
        assert example is None


@pytest.mark.django_db
class TestGetAllExamples:
    """Tests for get_all_examples function."""

    def test_get_all_examples_returns_list(self):
        """get_all_examples returns a list."""
        examples = get_all_examples()
        assert isinstance(examples, list)

    def test_get_all_examples_returns_all(self):
        """get_all_examples returns all examples."""
        examples = get_all_examples()
        assert len(examples) == len(EXAMPLES)


@pytest.mark.django_db
class TestHowToStep:
    """Tests for HowToStep class."""

    def test_howto_step_creation(self):
        """HowToStep can be created."""
        step = HowToStep(
            title='Test Step',
            description='Test description',
            code='print("test")',
            language='python',
        )
        assert step.title == 'Test Step'
        assert step.description == 'Test description'
        assert step.code == 'print("test")'
        assert step.language == 'python'

    def test_howto_step_default_language(self):
        """HowToStep defaults to python language."""
        step = HowToStep(
            title='Test',
            description='Desc',
            code='code',
        )
        assert step.language == 'python'


@pytest.mark.django_db
class TestExtractViewCode:
    """Tests for extract_view_code function."""

    def test_extract_view_code_returns_string(self):
        """extract_view_code returns a string."""
        code = extract_view_code(views.index_view)
        assert isinstance(code, str)

    def test_extract_view_code_contains_def(self):
        """extract_view_code result contains function code."""
        code = extract_view_code(views.index_view)
        assert len(code) > 0


@pytest.mark.django_db
class TestGetUrlPattern:
    """Tests for get_url_pattern function."""

    def test_get_url_pattern_returns_string(self):
        """get_url_pattern returns a string."""
        pattern = get_url_pattern('index')
        assert isinstance(pattern, str)

    def test_get_url_pattern_returns_valid_path(self):
        """get_url_pattern returns valid URL path."""
        pattern = get_url_pattern('active-search')
        assert pattern == '/active-search/'


@pytest.mark.django_db
class TestActiveSearchExample:
    """Tests for Active Search example configuration."""

    def test_active_search_example_exists(self):
        """Active Search example exists."""
        example = EXAMPLES.get('active-search')
        assert example is not None

    def test_active_search_has_steps(self):
        """Active Search has steps."""
        example = EXAMPLES['active-search']
        assert len(example.steps) > 0

    def test_active_search_has_doc_links(self):
        """Active Search has doc links."""
        example = EXAMPLES['active-search']
        assert len(example.doc_links) > 0

    def test_active_search_doc_links_structure(self):
        """Active Search doc links have correct structure."""
        example = EXAMPLES['active-search']
        for link in example.doc_links:
            assert 'title' in link
            assert 'url' in link


@pytest.mark.django_db
class TestTodoMVCExample:
    """Tests for TodoMVC example configuration."""

    def test_todo_mvc_example_exists(self):
        """TodoMVC example exists."""
        example = EXAMPLES.get('todo-mvc')
        assert example is not None

    def test_todo_mvc_has_steps(self):
        """TodoMVC has steps."""
        example = EXAMPLES['todo-mvc']
        assert len(example.steps) > 0

    def test_todo_mvc_steps_have_code(self):
        """TodoMVC steps have code."""
        example = EXAMPLES['todo-mvc']
        for step in example.steps:
            assert step.code is not None


@pytest.mark.django_db
class TestExampleContent:
    """Tests for example content quality."""

    def test_steps_have_titles(self):
        """All steps have titles."""
        for example in EXAMPLES.values():
            for step in example.steps:
                assert step.title is not None
                assert len(step.title) > 0

    def test_steps_have_descriptions(self):
        """All steps have descriptions."""
        for example in EXAMPLES.values():
            for step in example.steps:
                assert step.description is not None

    def test_steps_have_code(self):
        """All steps have code."""
        for example in EXAMPLES.values():
            for step in example.steps:
                assert step.code is not None

    def test_steps_have_valid_language(self):
        """All steps have valid language."""
        for example in EXAMPLES.values():
            for step in example.steps:
                assert step.language in ['python', 'html', 'django', 'javascript']
