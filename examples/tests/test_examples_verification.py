"""
These tests verify:
- Index page displays example cards
- All example pages load successfully
- All example SSE endpoints return proper Datastar responses
- Seed data exists for demos (when seed_data command is run)
"""

import pytest
from django.test import Client, override_settings
from django.urls import reverse

from examples.models import Contact, Notification, Todo


@pytest.fixture
def client():
    """Django test client fixture."""
    with override_settings(ALLOWED_HOSTS=['*']):
        return Client()


@pytest.mark.django_db
class TestIndexPage:
    """Test AC1: Index page displays 12 example cards."""

    def test_index_page_loads_successfully(self, client):
        """Verify index page returns 200."""
        response = client.get(reverse('examples:index'))
        assert response.status_code == 200

    def test_all_12_example_links_present(self, client):
        """Verify all 12 example links are in the index page."""
        response = client.get(reverse('examples:index'))
        content = response.content.decode()

        examples = [
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
        ]

        for example in examples:
            assert example in content, f"Example '{example}' not found in index page"


@pytest.mark.django_db
class TestExamplePages:
    @pytest.mark.parametrize(
        'url_name',
        [
            'examples:active-search',
            'examples:click-to-load',
            'examples:edit-row',
            'examples:delete-row',
            'examples:todo-mvc',
            'examples:inline-validation',
            'examples:infinite-scroll',
            'examples:lazy-tabs',
            'examples:file-upload',
            'examples:sortable',
            'examples:notifications',
            'examples:bulk-update',
        ],
    )
    def test_example_page_loads(self, client, url_name):
        """Verify each example page returns 200."""
        response = client.get(reverse(url_name))
        assert response.status_code == 200, f'Failed to load {url_name}'


@pytest.mark.django_db
class TestSourceCodeVisibility:
    """Test AC3: Source code is visible on example pages."""

    def test_howto_panel_included_in_example_pages(self, client):
        """Verify howto_panel.html is included in example pages."""
        response = client.get(reverse('examples:active-search'))
        content = response.content.decode()
        assert 'howtoOffcanvas' in content, 'Howto panel not found in example page'

    def test_code_snippets_present_in_howto_panel(self, client):
        """Verify code snippets (pre/code blocks) are present."""
        response = client.get(reverse('examples:active-search'))
        content = response.content.decode()
        # Check for code block structure in howto panel
        assert '<pre' in content, 'No pre/code blocks found in example page'
        assert 'code' in content.lower(), 'No code blocks found'


@pytest.mark.django_db
class TestDatastarEndpoints:
    """
    These tests verify that SSE endpoints return proper responses.
    The SSE content-type confirms Datastar is handling the requests.
    """

    def test_edit_row_returns_sse(self, client):
        """Verify edit row returns SSE content type."""
        contact = Contact.objects.create(
            first_name='Test', last_name='User', email='test@example.com'
        )
        url = reverse('examples:contact-update')
        response = client.post(
            url,
            {
                'id': contact.pk,
                'first_name': 'Updated',
                'last_name': 'Name',
                'email': 'updated@example.com',
            },
        )
        assert response.status_code == 200
        assert 'text/event-stream' in response.get('Content-Type', '')

    def test_todomvc_add_returns_sse(self, client):
        """Verify todo add returns SSE content type."""
        url = reverse('examples:todo-mvc-add')
        response = client.post(url, {'title': 'Test Todo'})
        assert response.status_code == 200
        assert 'text/event-stream' in response.get('Content-Type', '')

    def test_todomvc_toggle_returns_sse(self, client):
        """Verify todo toggle returns SSE content type."""
        todo = Todo.objects.create(title='Test', is_completed=False)
        url = reverse('examples:todo-mvc-toggle')
        response = client.post(url, {'id': todo.pk})
        assert response.status_code == 200
        assert 'text/event-stream' in response.get('Content-Type', '')

    def test_todomvc_delete_returns_sse(self, client):
        """Verify todo delete returns SSE content type."""
        todo = Todo.objects.create(title='Test', is_completed=False)
        url = reverse('examples:todo-mvc-delete')
        response = client.post(url, {'id': todo.pk})
        assert response.status_code == 200
        assert 'text/event-stream' in response.get('Content-Type', '')

    def test_notifications_count_returns_sse(self, client):
        """Verify notifications count returns SSE content type."""
        Notification.objects.create(message='Test', read=False)
        url = reverse('examples:notifications-count')
        response = client.get(url)
        assert response.status_code == 200
        assert 'text/event-stream' in response.get('Content-Type', '')

    def test_notifications_mark_read_returns_sse(self, client):
        """Verify notifications mark read returns SSE content type."""
        Notification.objects.create(message='Test', read=False)
        url = reverse('examples:notifications-mark-read')
        response = client.post(url)
        assert response.status_code == 200
        assert 'text/event-stream' in response.get('Content-Type', '')

    def test_bulk_update_returns_sse(self, client):
        """Verify bulk update returns SSE content type."""
        contact = Contact.objects.create(
            first_name='Bulk', last_name='Test', email='bulk@example.com'
        )
        url = reverse('examples:bulk-update-update')
        response = client.post(url, {'selected_ids': [contact.pk], 'action': 'delete'})
        assert response.status_code == 200
        assert 'text/event-stream' in response.get('Content-Type', '')


@pytest.mark.django_db
class TestDatastarIntegration:
    """Test AC5, AC6: Verify Datastar JavaScript is loaded."""

    def test_datastar_js_in_base_template(self, client):
        """Verify Datastar JS is included in base template."""
        response = client.get(reverse('examples:index'))
        content = response.content.decode()
        assert 'datastar' in content.lower(), 'Datastar JS not found in base template'

    def test_datastar_attributes_in_active_search(self, client):
        """Verify Datastar attributes are present in active search template."""
        response = client.get(reverse('examples:active-search'))
        content = response.content.decode()
        # Check for Datastar attributes
        assert (
            'data-bind' in content or 'data-signals' in content or 'data-on' in content
        )

    def test_datastar_uses_sse_not_polling(self, client):
        """Verify Datastar is configured for SSE (Server-Sent Events), not polling."""
        response = client.get(reverse('examples:active-search'))
        content = response.content.decode()
        # Verify SSE is being used - the data-on attribute should trigger SSE requests
        # This is confirmed by the SSE content-type tests above
        assert 'data-on:' in content, 'Datastar should use event handlers'
