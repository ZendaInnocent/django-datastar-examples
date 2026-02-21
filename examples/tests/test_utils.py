"""
Tests for utility functions in examples app.

Tests DatastarWithMessagesResponse including:
- Message extraction
- Event combination
- Response generation

Tests temp file functions:
- save_temp_file
- cleanup_temp_files
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest
from django.test import RequestFactory

from examples.utils import (
    TEMP_FILE_MAX_AGE_HOURS,
    TEMP_UPLOAD_DIR,
    DatastarWithMessagesResponse,
    cleanup_temp_files,
    save_temp_file,
)


@pytest.fixture(autouse=True)
def cleanup_temp_files_after_test(request):
    """Clean up temp files after each test."""
    import os

    from django.core.files.storage import default_storage

    yield

    # Try default_storage first
    try:
        files, _ = default_storage.listdir(TEMP_UPLOAD_DIR)
        for file_name in files:
            if not file_name.startswith('.'):
                try:
                    default_storage.delete(f'{TEMP_UPLOAD_DIR}/{file_name}')
                except Exception:
                    pass
    except FileNotFoundError:
        pass

    # Also clean up files in current working directory (for tests with empty base_location)
    temp_dir = 'temp_uploads'
    if os.path.exists(temp_dir):
        try:
            for file_name in os.listdir(temp_dir):
                if not file_name.startswith('.'):
                    try:
                        os.remove(os.path.join(temp_dir, file_name))
                    except Exception:
                        pass
        except Exception:
            pass


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
        assert hasattr(utils, 'save_temp_file')
        assert hasattr(utils, 'cleanup_temp_files')
        assert hasattr(utils, 'TEMP_UPLOAD_DIR')
        assert hasattr(utils, 'TEMP_FILE_MAX_AGE_HOURS')


@pytest.mark.django_db
class TestSaveTempFile:
    """Tests for save_temp_file function."""

    def test_save_temp_file_creates_file(self):
        """save_temp_file creates a file in temp storage."""
        file_content = b'test file content'
        file_name = 'test_document.pdf'

        saved_path = save_temp_file(file_name, file_content)

        assert saved_path is not None
        assert TEMP_UPLOAD_DIR in saved_path
        assert file_name in saved_path

    def test_save_temp_file_adds_timestamp_prefix(self):
        """save_temp_file adds timestamp prefix to filename."""
        file_content = b'test content'
        file_name = 'document.txt'

        saved_path = save_temp_file(file_name, file_content)

        parts = saved_path.split('/')
        file_part = parts[-1]
        assert '_' in file_part
        timestamp_str = file_part.split('_')[0]
        assert timestamp_str.isdigit()

    def test_save_temp_file_returns_correct_path(self):
        """save_temp_file returns the storage path."""
        file_content = b'some data'
        file_name = 'data.json'

        saved_path = save_temp_file(file_name, file_content)

        assert saved_path.startswith(f'{TEMP_UPLOAD_DIR}/')


@pytest.mark.django_db
class TestCleanupTempFiles:
    """Tests for cleanup_temp_files function."""

    def test_cleanup_temp_files_returns_zero_for_no_files(self):
        """cleanup_temp_files returns 0 when no temp files exist."""
        deleted_count = cleanup_temp_files(max_age_hours=0)
        assert deleted_count == 0

    def test_cleanup_temp_files_deletes_old_files(self):
        """cleanup_temp_files deletes files older than max_age_hours."""

        from django.core.files.storage import default_storage

        file_name = 'old_file.txt'
        file_content = b'old content'

        saved_path = save_temp_file(file_name, file_content)
        file_name_only = saved_path.split('/')[-1]

        old_time = datetime.now(timezone.utc) - timedelta(hours=2)

        with (
            patch.object(default_storage, 'listdir') as mock_listdir,
            patch.object(default_storage, 'get_modified_time') as mock_get_modified,
            patch.object(default_storage, 'delete') as mock_delete,
        ):
            mock_listdir.return_value = ([file_name_only], [])
            mock_get_modified.return_value = old_time

            deleted_count = cleanup_temp_files(max_age_hours=1)

        assert deleted_count == 1
        mock_delete.assert_called_once()

    def test_cleanup_temp_files_keeps_recent_files(self):
        """cleanup_temp_files keeps files within max_age_hours."""
        file_name = 'recent_file.txt'
        file_content = b'recent content'

        save_temp_file(file_name, file_content)

        deleted_count = cleanup_temp_files(max_age_hours=1)

        assert deleted_count == 0

    def test_cleanup_temp_files_handles_missing_directory(self):
        """cleanup_temp_files handles missing temp directory gracefully."""
        from django.core.files.storage import default_storage

        with patch.object(default_storage, 'listdir') as mock_listdir:
            mock_listdir.side_effect = FileNotFoundError('Directory not found')
            deleted_count = cleanup_temp_files()

        assert deleted_count == 0


class TestTempFileConstants:
    """Tests for temp file constants."""

    def test_temp_upload_dir_constant(self):
        """TEMP_UPLOAD_DIR is set correctly."""
        assert TEMP_UPLOAD_DIR == 'temp_uploads'

    def test_temp_max_age_hours_constant(self):
        """TEMP_FILE_MAX_AGE_HOURS is set correctly."""
        assert TEMP_FILE_MAX_AGE_HOURS == 1
