import time

from datastar_py import ServerSentEventGenerator as SSE
from datastar_py import consts
from datastar_py.django import DatastarResponse
from django.contrib import messages
from django.template.loader import render_to_string

TEMP_UPLOAD_DIR = 'temp_uploads'
TEMP_FILE_MAX_AGE_HOURS = 1


class DatastarWithMessagesResponse(DatastarResponse):
    def __init__(self, request, events=None, **kwargs):
        current_messages = messages.get_messages(request)
        message_events = []

        for msg in current_messages:
            html = render_to_string('examples/fragments/alert.html', {'message': msg})
            message_events.append(
                SSE.patch_elements(
                    html,
                    '#message-container',
                    consts.ElementPatchMode.APPEND,
                    use_view_transition=True,
                )
            )

        all_events = message_events + (
            [events]
            if events and not isinstance(events, list)
            else (events if events else [])
        )
        super().__init__(all_events, **kwargs)


def save_temp_file(file_name: str, content: bytes) -> str:
    from django.core.files.base import ContentFile
    from django.core.files.storage import default_storage

    timestamp = int(time.time())
    temp_name = f'{timestamp}_{file_name}'
    content_file = ContentFile(content, name=temp_name)
    path = default_storage.save(f'{TEMP_UPLOAD_DIR}/{temp_name}', content_file)
    return path


def cleanup_temp_files(max_age_hours: int = TEMP_FILE_MAX_AGE_HOURS) -> int:
    from django.core.files.storage import default_storage

    deleted_count = 0
    cutoff_time = time.time() - (max_age_hours * 3600)

    try:
        files, dirs = default_storage.listdir(TEMP_UPLOAD_DIR)
        for file_name in files:
            if file_name.startswith('.'):
                continue
            try:
                file_path = f'{TEMP_UPLOAD_DIR}/{file_name}'
                file_age = default_storage.get_modified_time(file_path).timestamp()
                if file_age < cutoff_time:
                    default_storage.delete(file_path)
                    deleted_count += 1
            except Exception:
                pass
    except FileNotFoundError:
        pass

    return deleted_count
