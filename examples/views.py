from datastar_py import consts
from datastar_py.django import DatastarResponse, datastar_response, read_signals
from datastar_py.django import ServerSentEventGenerator as SSE
from django.core.paginator import Paginator
from django.core.validators import ValidationError, validate_email
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Contact, Item, Notification, Todo


def index_view(request):
    return render(request, 'examples/index.html')


# ============================================================================
# 1. Active Search
# ============================================================================


def active_search_view(request):
    if request.headers.get('Datastar-Request'):
        signals = read_signals(request)
        query = signals.get('search', '').strip()

        if query is not None:
            contacts = Contact.objects.filter(
                models.Q(first_name__icontains=query)
                | models.Q(last_name__icontains=query)
                | models.Q(email__icontains=query)
            )[:10]
        else:
            contacts = Contact.objects.none()

        html = render_to_string(
            'examples/fragments/contact_list.html', {'contacts': contacts}
        )

        return DatastarResponse(
            SSE.patch_elements(html, selector='#contact-list'),
        )

    contacts = Contact.objects.all()[:10]
    return render(request, 'examples/active_search.html', {'contacts': contacts})


# ============================================================================
# 2. Click to Load
# ============================================================================


def click_to_load_view(request):
    page = 1
    contacts = Contact.objects.all()
    items_per_page = 2
    paginator = Paginator(contacts, items_per_page)
    page_obj = paginator.get_page(page)

    if request.headers.get('Datastar-Request'):
        signals = read_signals(request)
        page = signals.get('page')

        if page is not None:
            page_obj = paginator.get_page(page)
            html = render_to_string(
                'examples/fragments/contact_list_append.html',
                {'contacts': page_obj},
            )

            return DatastarResponse(
                [
                    SSE.patch_elements(
                        html,
                        selector='#contact-list',
                        mode=consts.ElementPatchMode.APPEND,
                    ),
                    SSE.patch_signals({'hasMore': page_obj.has_next()}),
                ]
            )

    return render(
        request,
        'examples/click_to_load.html',
        {'contacts': page_obj},
    )


# ============================================================================
# 3. Edit Row
# ============================================================================


def edit_row_view(request):
    contacts = Contact.objects.all()[:10]
    return render(request, 'examples/edit_row.html', {'contacts': contacts})


@csrf_exempt
def contact_update_view(request):
    signals = read_signals(request)
    contact_id = signals.get('contactId')
    contact = get_object_or_404(Contact, pk=contact_id)

    if request.method == 'POST':
        first_name = signals.get('first_name')
        last_name = signals.get('last_name')
        email = signals.get('email')

        contact.first_name = first_name
        contact.last_name = last_name
        contact.email = email
        contact.save()
        html = render_to_string(
            'examples/fragments/contact_row.html', {'contact': contact}
        )
        return DatastarResponse(
            SSE.patch_elements(html, selector=f'#contact-{contact.pk}'),
        )

    return DatastarResponse(
        SSE.patch_elements(
            render_to_string(
                'examples/fragments/contact_form.html',
                {'contact': contact},
            ),
            selector=f'#contact-{contact.pk}',
        )
    )


# ============================================================================
# 4. Delete Row
# ============================================================================


@csrf_exempt
def delete_row_view(request):
    if request.headers.get('Datastar-Request'):
        signals = read_signals(request)
        contact_id = signals.get('contactId')
        contact = get_object_or_404(Contact, pk=contact_id)
        contact.delete()

        return DatastarResponse(SSE.remove_elements(selector=f'#contact-{contact_id}'))

    contacts = Contact.objects.all()
    return render(request, 'examples/delete_row.html', {'contacts': contacts})


# ============================================================================
# 5. TodoMVC
# ============================================================================


def todomvc_view(request):
    todos = Todo.objects.all()
    return render(
        request,
        'examples/todomvc.html',
        {
            'todos': todos,
            'total_count': Todo.objects.count(),
            'active_count': Todo.objects.filter(completed=False).count(),
            'completed_count': Todo.objects.filter(completed=True).count(),
        },
    )


@require_http_methods(['POST'])
@datastar_response
def todomvc_add_view(request):
    title = request.POST.get('title', '').strip()

    if title:
        max_order = Todo.objects.order_by('-order').first()
        new_order = (max_order.order + 1) if max_order else 0
        todo = Todo.objects.create(title=title, order=new_order)

        html = render_to_string('examples/fragments/todo_item.html', {'todo': todo})
        yield SSE.patch_elements(
            html,
            selector='#todo-list',
            mode=consts.ElementPatchMode.PREPEND,
        )


@csrf_exempt
@require_http_methods(['POST'])
@datastar_response
def todomvc_toggle_view(request):
    signals = read_signals(request)
    todo_id = signals.get('todoToggleId')

    todo = get_object_or_404(Todo, pk=todo_id)
    todo.completed = not todo.completed
    todo.save()

    html = render_to_string('examples/fragments/todo_item.html', {'todo': todo})
    yield SSE.patch_elements(
        html,
        selector=f'#todo-{todo_id}',
        mode=consts.ElementPatchMode.REPLACE,
    )
    yield SSE.patch_signals(
        {
            'activeCount': Todo.objects.filter(completed=False).count(),
        }
    )


@csrf_exempt
@require_http_methods(['POST'])
@datastar_response
def todomvc_delete_view(request):
    signals = read_signals(request)
    todo_id = signals.get('todoToggleId')
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.delete()

    yield SSE.remove_elements(selector=f'#todo-{todo_id}')


@csrf_exempt
@require_http_methods(['POST'])
@datastar_response
def todomvc_clear_view(request):
    Todo.objects.filter(completed=True).delete()

    todos = Todo.objects.all()
    html = render_to_string('examples/fragments/todo_list.html', {'todos': todos})
    yield SSE.patch_elements(html, selector='#todo-list')
    yield SSE.patch_signals({'filter': 'all'})


@datastar_response
def todomvc_filter_view(request):
    signals = read_signals(request)
    if signals is not None:
        filter_type = signals.get('filter')
    else:
        filter_type = 'all'

    todos = Todo.objects.all()

    if filter_type == 'active':
        todos = todos.filter(completed=False)
    elif filter_type == 'completed':
        todos = todos.filter(completed=True)

    html = render_to_string('examples/fragments/todo_list.html', {'todos': todos})
    yield SSE.patch_elements(html, selector='#todo-list')


@datastar_response
def get_contact_view(request):
    signals = read_signals(request)
    contact_id = signals.get('contactId')
    contact = get_object_or_404(Contact, pk=contact_id)
    html = render_to_string('examples/fragments/contact_row.html', {'contact': contact})
    yield SSE.patch_elements(html, f'#contact-{contact.pk}')


# ============================================================================
# 6. Inline Validation
# ============================================================================


def inline_validation_view(request):
    return render(request, 'examples/inline_validation.html')


@datastar_response
def inline_validation_validate_view(request):
    field = request.GET.get('field')
    value = request.GET.get('value', '')

    errors = {}
    if field == 'email':
        try:
            validate_email(value)
        except ValidationError:
            errors['email'] = 'Please enter a valid email address'

    if field == 'username':
        if len(value) < 3:
            errors['username'] = 'Username must be at least 3 characters'
        elif not value.isalnum():
            errors['username'] = 'Username must contain only letters and numbers'

    if field == 'password':
        if len(value) < 6:
            errors['password'] = 'Password must be at least 6 characters'

    html = render_to_string(
        'examples/fragments/validation_error.html',
        {'field': field, 'errors': errors},
    )
    yield SSE.patch_elements(html, selector=f'#{field}-error')


# ============================================================================
# 7. Infinite Scroll
# ============================================================================


def infinite_scroll_view(request):
    page = 1
    items_per_page = 6
    contacts = Contact.objects.all()
    paginator = Paginator(contacts, items_per_page)
    page_obj = paginator.get_page(page)

    if request.headers.get('Datastar-Request'):
        signals = read_signals(request)
        page = signals.get('page')

        if page is not None:
            page_obj = paginator.get_page(page)
            html = render_to_string(
                'examples/fragments/contact_list_append.html',
                {'contacts': page_obj},
            )
            return DatastarResponse(
                [
                    SSE.patch_signals({'hasMore': page_obj.has_next()}),
                    SSE.patch_elements(
                        html,
                        selector='#contact-list',
                        mode=consts.ElementPatchMode.APPEND,
                    ),
                ]
            )

    return render(
        request,
        'examples/infinite_scroll.html',
        {'contacts': page_obj},
    )


# ============================================================================
# 8. Lazy Tabs
# ============================================================================


def lazy_tabs_view(request):
    if request.headers.get('Datastar-Request'):
        signals = read_signals(request)
        tab = signals.get('activeTab', 'home')

        content = {
            'home': 'Welcome to the home tab! This content was loaded lazily.',
            'about': 'About Us: We build modern web applications with Django and Datastar.',
            'contact': 'Contact us at: hello@example.com',
        }.get(tab, 'Content not found')

        html = render_to_string(
            'examples/fragments/tab_content.html', {'content': content}
        )
        return DatastarResponse(
            [
                SSE.patch_elements(html, selector='#tab-content'),
                SSE.patch_signals({'activeTab': tab}),
            ]
        )

    return render(request, 'examples/lazy_tabs.html')


# ============================================================================
# 9. File Upload
# ============================================================================


def file_upload_view(request):
    if request.headers.get('Datastar-Request'):
        if request.method == 'POST':
            uploaded_file = request.FILES.get('file')

            if uploaded_file:
                result = f'Uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)'
            else:
                result = 'No file uploaded'

            html = render_to_string(
                'examples/fragments/upload_result.html', {'result': result}
            )
            return DatastarResponse(SSE.patch_elements(html, selector='#upload-result'))

    return render(request, 'examples/file_upload.html')


# ============================================================================
# 10. Sortable
# ============================================================================


def sortable_view(request):
    if request.headers.get('Datastar-Request'):
        signals = read_signals(request)
        current_order = signals.get('order')

        new_ordered_todos = []

        for index, item_pk in enumerate(current_order, start=1):
            item = Item.objects.get(pk=item_pk)
            item.order = index
            new_ordered_todos.append(item)

        Item.objects.bulk_update(new_ordered_todos, fields=['order'])
        return

    items = Item.objects.all()
    return render(request, 'examples/sortable.html', {'items': items})


# ============================================================================
# 11. Notifications
# ============================================================================


def notifications_view(request):
    notifications = Notification.objects.all()[:5]
    unread_count = Notification.objects.filter(read=False).count()
    return render(
        request,
        'examples/notifications.html',
        {'notifications': notifications, 'unread_count': unread_count},
    )


@datastar_response
def notifications_count_view(request):
    unread_count = Notification.objects.filter(read=False).count()
    yield SSE.patch_signals({'count': unread_count})


@datastar_response
def notifications_mark_read_view(request):
    Notification.objects.filter(read=False).update(read=True)

    html = render_to_string(
        'examples/fragments/notification_list.html',
        {'notifications': Notification.objects.all()[:5], 'unread_count': 0},
    )
    yield SSE.patch_elements(html, selector='#notifications-list')


# ============================================================================
# 12. Bulk Update
# ============================================================================


def bulk_update_view(request):
    contacts = Contact.objects.all()[:10]
    return render(request, 'examples/bulk_update.html', {'contacts': contacts})


@datastar_response
def bulk_update_update_view(request):
    selected_ids = request.POST.getlist('selected_ids')
    action = request.POST.get('action')

    if action == 'delete' and selected_ids:
        Contact.objects.filter(pk__in=selected_ids).delete()

    remaining_contacts = Contact.objects.all()[:10]
    html = render_to_string(
        'examples/fragments/contact_table.html', {'contacts': remaining_contacts}
    )
    yield SSE.patch_elements(html, selector='#contact-table')


# ============================================================================
# Search Functionality (Story 4.1)
# ============================================================================


def search_view(request):
    """Search page view (for direct URL access)."""
    query = request.GET.get('q', '')
    results = []

    if query:
        from .search import search as perform_search

        results = perform_search(query)

    return render(request, 'examples/search.html', {'results': results, 'query': query})


@datastar_response
def search_instant_view(request):
    """Datastar endpoint for instant search results."""
    signals = read_signals(request)
    query = signals.get('search_query', '').strip()

    if not query:
        # Return empty state
        html = render_to_string(
            'examples/fragments/search_results.html',
            {'results': [], 'query': query, 'empty': True},
        )
        yield SSE.patch_elements(html, selector='#search-results')
        return

    # Perform search
    from .search import search as perform_search

    results = perform_search(query, limit=10)

    html = render_to_string(
        'examples/fragments/search_results.html', {'results': results, 'query': query}
    )
    yield SSE.patch_elements(html, selector='#search-results')
