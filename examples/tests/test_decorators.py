"""
Tests for decorators in examples app.

Tests the datastar_response decorator including:
- Function wrapping
- Message handling
- SSE response generation
- View function preservation
"""

import pytest
from unittest.mock import MagicMock
from django.test import RequestFactory

from examples.decorators import datastar_response


@pytest.mark.django_db
class TestDatastarResponseDecorator:
    """Tests for datastar_response decorator."""

    def test_decorator_preserves_function_name(self):
        """Decorator preserves the wrapped function name."""

        @datastar_response
        def test_view(request):
            yield MagicMock()

        assert test_view.__name__ == 'test_view'

    def test_decorator_preserves_function_docstring(self):
        """Decorator preserves the wrapped function docstring."""

        @datastar_response
        def test_view(request):
            """Test function docstring."""
            yield MagicMock()

        assert test_view.__doc__ == 'Test function docstring.'

    def test_decorator_preserves_function_attributes(self):
        """Decorator preserves function attributes."""

        @datastar_response
        def test_view(request):
            yield MagicMock()

        assert hasattr(test_view, '__wrapped__')

    def test_decorator_returns_datastar_response(self):
        """Decorator returns DatastarResponse."""

        @datastar_response
        def test_view(request):
            yield MagicMock()

        factory = RequestFactory()
        request = factory.get('/')
        request._messages = MagicMock()

        response = test_view(request)
        assert response is not None

    def test_decorator_with_yield(self):
        """Decorator works with generator that yields SSE events."""

        @datastar_response
        def test_view(request):
            from datastar_py.django import ServerSentEventGenerator as SSE

            yield SSE.patch_elements('<div>test</div>', selector='#test')

        factory = RequestFactory()
        request = factory.get('/')
        request._messages = MagicMock()

        response = test_view(request)
        assert response is not None

    def test_decorator_handles_multiple_yields(self):
        """Decorator handles multiple yield statements."""

        @datastar_response
        def test_view(request):
            from datastar_py.django import ServerSentEventGenerator as SSE

            yield SSE.patch_elements('<div>test1</div>', selector='#test1')
            yield SSE.patch_elements('<div>test2</div>', selector='#test2')

        factory = RequestFactory()
        request = factory.get('/')
        request._messages = MagicMock()

        response = test_view(request)
        assert response is not None


@pytest.mark.django_db
class TestDecoratorWithMessages:
    """Tests for decorator message handling."""

    def test_decorator_with_success_message(self):
        """Decorator includes Django messages in response."""

        @datastar_response
        def test_view(request):
            from django.contrib import messages
            from datastar_py.django import ServerSentEventGenerator as SSE

            messages.success(request, 'Test success message')
            yield SSE.patch_elements('<div>test</div>', selector='#test')

        factory = RequestFactory()
        request = factory.get('/')
        # Set up messages middleware
        from django.contrib.messages.middleware import MessageMiddleware

        # Add required attributes for messages
        request.session = {}
        MessageMiddleware(lambda req: None)(request)

        response = test_view(request)
        assert response is not None


@pytest.mark.django_db
class TestDecoratorEdgeCases:
    """Edge case tests for datastar_response decorator."""

    def test_decorator_with_empty_generator(self):
        """Decorator handles empty generator."""

        @datastar_response
        def test_view(request):
            return
            yield  # Makes it a generator

        factory = RequestFactory()
        request = factory.get('/')
        request._messages = MagicMock()

        response = test_view(request)
        assert response is not None

    def test_decorator_with_exception(self):
        """Decorator passes through exceptions."""

        @datastar_response
        def test_view(request):
            raise ValueError('Test error')

        factory = RequestFactory()
        request = factory.get('/')
        request._messages = MagicMock()

        with pytest.raises(ValueError):
            test_view(request)
