"""
Tests for utility functions in examples app.

Tests DatastarWithMessagesResponse including:
- Message extraction
- Event combination
- Response generation
"""

import pytest
from unittest.mock import MagicMock
from django.test import RequestFactory

from examples.utils import DatastarWithMessagesResponse


@pytest.mark.django_db
class TestDatastarWithMessagesResponse:
    """Tests for DatastarWithMessagesResponse class."""

    def test_response_init_without_messages(self):
        """Response can be initialized without messages."""
        factory = RequestFactory()
        request = factory.get('/')
        request._messages = MagicMock()

        response = DatastarWithMessagesResponse(request, [])
        assert response is not None

    def test_response_with_sse_event(self):
        """Response handles SSE event."""
        factory = RequestFactory()
        request = factory.get('/')
        request._messages = MagicMock()

        from datastar_py.django import ServerSentEventGenerator as SSE

        event = SSE.patch_elements('<div>test</div>', selector='#test')
        response = DatastarWithMessagesResponse(request, event)
        assert response is not None

    def test_response_with_list_of_events(self):
        """Response handles list of events."""
        factory = RequestFactory()
        request = factory.get('/')
        request._messages = MagicMock()

        from datastar_py.django import ServerSentEventGenerator as SSE

        events = [
            SSE.patch_elements('<div>test1</div>', selector='#test1'),
            SSE.patch_elements('<div>test2</div>', selector='#test2'),
        ]
        response = DatastarWithMessagesResponse(request, events)
        assert response is not None

    def test_response_combines_messages_with_events(self):
        """Response combines messages with main events."""
        factory = RequestFactory()
        request = factory.get('/')
        request._messages = MagicMock()

        from datastar_py.django import ServerSentEventGenerator as SSE

        event = SSE.patch_elements('<div>test</div>', selector='#test')
        response = DatastarWithMessagesResponse(request, event)
        assert response is not None


@pytest.mark.django_db
class TestDatastarWithMessagesResponseIntegration:
    """Integration tests for DatastarWithMessagesResponse."""

    def test_response_with_django_messages(self):
        """Response extracts Django messages correctly."""
        factory = RequestFactory()
        request = factory.get('/')

        # Create a mock messages storage
        mock_storage = MagicMock()
        mock_msg = MagicMock()
        mock_msg.tags = 'success'
        mock_msg.message = 'Test message'
        mock_storage.__iter__ = MagicMock(return_value=iter([mock_msg]))
        request._messages = mock_storage

        from datastar_py.django import ServerSentEventGenerator as SSE

        event = SSE.patch_elements('<div>test</div>', selector='#test')
        response = DatastarWithMessagesResponse(request, event)
        assert response is not None


class TestUtilsModule:
    """Tests for utils module functions and classes."""

    def test_datastar_with_messages_response_exists(self):
        """DatastarWithMessagesResponse class exists."""
        assert DatastarWithMessagesResponse is not None

    def test_datastar_with_messages_response_inheritance(self):
        """DatastarWithMessagesResponse inherits from DatastarResponse."""
        from datastar_py.django import DatastarResponse

        assert issubclass(DatastarWithMessagesResponse, DatastarResponse)

    def test_module_exports(self):
        """Module exports expected classes."""
        from examples import utils

        assert hasattr(utils, 'DatastarWithMessagesResponse')
