from datastar_py import ServerSentEventGenerator as SSE
from datastar_py.django import DatastarResponse
from django.contrib import messages
from django.template.loader import render_to_string


class DatastarWithMessagesResponse(DatastarResponse):
    def __init__(self, request, events=None, **kwargs):
        current_messages = messages.get_messages(request)
        message_events = []

        for msg in current_messages:
            html = render_to_string('examples/fragments/alert.html', {'message': msg})
            message_events.append(
                SSE.patch_elements(html, '#message-container', use_view_transition=True)
            )

        all_events = message_events + (
            [events]
            if events and not isinstance(events, list)
            else (events if events else [])
        )
        super().__init__(all_events, **kwargs)
