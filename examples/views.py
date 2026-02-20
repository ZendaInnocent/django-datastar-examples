import time

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
    return render(
        request,
        'examples/active_search.html',
        {'contacts': contacts, 'howto_slug': 'active-search'},
    )


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
        {'contacts': page_obj, 'howto_slug': 'click-to-load'},
    )


# ============================================================================
# 3. Edit Row
# ============================================================================


def edit_row_view(request):
    contacts = Contact.objects.all()[:10]
    return render(
        request,
        'examples/edit_row.html',
        {'contacts': contacts, 'howto_slug': 'edit-row'},
    )


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


@datastar_response
def get_contact_view(request):
    signals = read_signals(request)
    contact_id = signals.get('contactId')
    contact = get_object_or_404(Contact, pk=contact_id)
    html = render_to_string('examples/fragments/contact_row.html', {'contact': contact})
    yield SSE.patch_elements(html, f'#contact-{contact.pk}')


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
    return render(
        request,
        'examples/delete_row.html',
        {'contacts': contacts, 'howto_slug': 'delete-row'},
    )


# ============================================================================
# 5. TodoMVC
# ============================================================================


def get_todo_counts():
    counts = Todo.objects.aggregate(
        completed=models.Count('pk', filter=models.Q(is_completed=True)),
        active=models.Count('pk', filter=models.Q(is_completed=False)),
    )
    return counts


def todomvc_view(request):
    todos = Todo.objects.all()
    counts = get_todo_counts()

    return render(
        request,
        'examples/todomvc.html',
        {
            'todos': todos,
            'count_todos_active': counts.get('active'),
            'count_todos_completed': counts.get('completed'),
            'howto_slug': 'todo-mvc',
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

        counts = get_todo_counts()
        yield SSE.patch_signals({'activeCount': counts.get('active')})


@csrf_exempt
@require_http_methods(['POST'])
@datastar_response
def todomvc_toggle_view(request):
    signals = read_signals(request)
    todo_id = signals.get('todoToggleId')
    filter = signals.get('filter')

    todo = get_object_or_404(Todo, pk=todo_id)
    todo.is_completed = not todo.is_completed
    todo.save()

    html = render_to_string('examples/fragments/todo_item.html', {'todo': todo})

    if filter == 'all':
        mode = consts.ElementPatchMode.REPLACE
    else:
        mode = consts.ElementPatchMode.REMOVE

    counts = get_todo_counts()

    yield SSE.patch_elements(html, selector=f'#todo-{todo_id}', mode=mode)
    yield SSE.patch_signals(
        {
            'activeCount': counts.get('active'),
            'completedCount': counts.get('completed'),
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

    counts = get_todo_counts()

    yield SSE.remove_elements(selector=f'#todo-{todo_id}')
    yield SSE.patch_signals(
        {
            'activeCount': counts.get('active'),
            'completedCount': counts.get('completed'),
        }
    )


@csrf_exempt
@require_http_methods(['POST'])
@datastar_response
def todomvc_clear_view(request):
    Todo.objects.filter(is_completed=True).delete()

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
        todos = todos.filter(is_completed=False)
    elif filter_type == 'completed':
        todos = todos.filter(is_completed=True)

    html = render_to_string('examples/fragments/todo_list.html', {'todos': todos})
    yield SSE.patch_elements(html, selector='#todo-list')


# ============================================================================
# 6. Inline Validation
# ============================================================================


def inline_validation_view(request):
    return render(
        request,
        'examples/inline_validation.html',
        {'howto_slug': 'inline-validation'},
    )


@datastar_response
def inline_validation_validate_view(request):
    signals = read_signals(request)
    field = signals.get('field')

    errors = {}
    if field == 'email':
        value = signals.get('email')
        try:
            validate_email(value)
        except ValidationError:
            errors['email'] = 'Please enter a valid email address'

    if field == 'username':
        value = signals.get('username')
        if len(value) < 3:
            errors['username'] = 'Username must be at least 3 characters'
        elif not value.isalnum():
            errors['username'] = 'Username must contain only letters and numbers'

    if field == 'password':
        value = signals.get('password')
        if len(value) < 6:
            errors['password'] = 'Password must be at least 6 characters'

    html = render_to_string(
        'examples/fragments/validation_error.html',
        {'field': field, 'error': errors.get(field)},
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
        {'contacts': page_obj, 'howto_slug': 'infinite-scroll'},
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

    return render(
        request,
        'examples/lazy_tabs.html',
        {'howto_slug': 'lazy-tabs'},
    )


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

    return render(
        request,
        'examples/file_upload.html',
        {'howto_slug': 'file-upload'},
    )


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
    return render(
        request,
        'examples/sortable.html',
        {'items': items, 'howto_slug': 'sortable'},
    )


# ============================================================================
# 11. Notifications
# ============================================================================


def notifications_view(request):
    return render(
        request,
        'examples/notifications.html',
        {'howto_slug': 'notifications'},
    )


@datastar_response
def notifications_sse_view(request):
    notifications = Notification.objects.filter(read=False)

    for notification in notifications:
        alert = render_to_string(
            'examples/fragments/notification_alert.html',
            {'notification': notification},
        )

        yield SSE.patch_elements(
            alert, selector='#notifications-list', mode=consts.ElementPatchMode.APPEND
        )
        time.sleep(3)


@datastar_response
def notifications_count_view(request):
    unread_count = Notification.objects.filter(read=False).count()
    yield SSE.patch_signals({'notificationCount': unread_count})


@csrf_exempt
@datastar_response
def notifications_mark_read_view(request):
    signals = read_signals(request)
    notification_id = signals.get('notificationId')

    if notification_id:
        notification = get_object_or_404(Notification, pk=notification_id)
        notification.read = True
        notification.save()
        yield SSE.patch_signals(
            {'notificationCount': Notification.objects.filter(read=False).count()}
        )
    else:
        Notification.objects.filter(read=False).update(read=True)

        yield SSE.patch_signals(
            {'notificationCount': Notification.objects.filter(read=False).count()}
        )
        html = render_to_string(
            'examples/fragments/notification_list.html',
            {'notifications': Notification.objects.filter(read=False)},
        )
        yield SSE.patch_elements(html, selector='#notifications-list')


# ============================================================================
# 12. Bulk Update
# ============================================================================


def bulk_update_view(request):
    contacts = Contact.objects.all()[:10]
    return render(
        request,
        'examples/bulk_update.html',
        {'contacts': contacts, 'howto_slug': 'bulk-update'},
    )


@csrf_exempt
@datastar_response
def bulk_update_update_view(request):
    selected_ids = request.POST.getlist('selected_ids')
    action = request.POST.get('action')

    if action == 'activate' and selected_ids:
        Contact.objects.filter(pk__in=selected_ids).update(is_active=True)

    if action == 'deactivate' and selected_ids:
        Contact.objects.filter(pk__in=selected_ids).update(is_active=False)

    contacts = Contact.objects.all()[:10]
    html = render_to_string(
        'examples/fragments/contact_table.html', {'contacts': contacts}
    )
    yield SSE.patch_elements(html, selector='#contact-table')


# ============================================================================
# Search Functionality
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
