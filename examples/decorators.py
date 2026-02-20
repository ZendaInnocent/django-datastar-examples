from functools import wraps

from datastar_py import consts
from datastar_py.django import DatastarResponse
from datastar_py.django import ServerSentEventGenerator as SSE
from django.contrib.messages import get_messages
from django.template.loader import render_to_string


def datastar_response(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        generator = view_func(request, *args, **kwargs)

        def stream():
            # First yield everything from the view
            yield from generator

            # Then automatically emit messages
            storage = get_messages(request)

            for msg in storage:
                yield SSE.patch_elements(
                    render_to_string('examples/fragments/alert.html', {'message': msg}),
                    '#message-container',
                    consts.ElementPatchMode.APPEND,
                )

        return DatastarResponse(stream())

    return wrapper
