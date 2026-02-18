from datastar_py import consts
from datastar_py.django import ServerSentEventGenerator as SSE
from datastar_py.django import datastar_response, read_signals
from django import forms
from django.core.validators import ValidationError, validate_email
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from .models import Contact, Item, Notification, Todo


def index_view(request):
    return render(request, 'examples/index.html')


# ============================================================================
# 1. Active Search
# ============================================================================


def active_search_view(request):
    contacts = Contact.objects.all()[:10]
    return render(request, 'examples/active_search.html', {'contacts': contacts})


@datastar_response
def active_search_search_view(request):
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
    yield SSE.patch_elements(html, selector='#results')


# ============================================================================
# 2. Click to Load
# ============================================================================


def click_to_load_view(request):
    page = int(request.GET.get('page', 1))
    items_per_page = 6
    items = Contact.objects.all()[(page - 1) * items_per_page : page * items_per_page]
    has_more = Contact.objects.count() > page * items_per_page
    return render(
        request,
        'examples/click_to_load.html',
        {'contacts': items, 'page': page, 'has_more': has_more},
    )


@datastar_response
def click_to_load_more_view(request):
    page = int(request.GET.get('page', 1))
    items_per_page = 6
    contacts = Contact.objects.all()[
        (page - 1) * items_per_page : page * items_per_page
    ]
    has_more = Contact.objects.count() > page * items_per_page

    html = render_to_string(
        'examples/fragments/contact_list.html',
        {'contacts': contacts, 'page': page, 'has_more': has_more},
    )
    yield SSE.patch_elements(
        html, selector='#contact-list', mode=consts.ElementPatchMode.APPEND
    )


# ============================================================================
# 3. Edit Row
# ============================================================================


def edit_row_view(request):
    contacts = Contact.objects.all()[:5]
    return render(request, 'examples/edit_row.html', {'contacts': contacts})


@datastar_response
def edit_row_update_view(request):
    contact_id = request.POST.get('id')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')

    contact = get_object_or_404(Contact, pk=contact_id)
    contact.first_name = first_name
    contact.last_name = last_name
    contact.email = email
    contact.save()

    html = render_to_string('examples/fragments/contact_row.html', {'contact': contact})
    yield SSE.patch_elements(html, selector=f'#contact-{contact_id}')


# ============================================================================
# 4. Delete Row
# ============================================================================


def delete_row_view(request):
    contacts = Contact.objects.all()[:5]
    return render(request, 'examples/delete_row.html', {'contacts': contacts})


@datastar_response
def delete_row_remove_view(request):
    contact_id = request.POST.get('id')
    contact = get_object_or_404(Contact, pk=contact_id)
    contact.delete()

    yield SSE.remove_elements(selector=f'#contact-{contact_id}')


# ============================================================================
# 5. TodoMVC
# ============================================================================


def todomvc_view(request):
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'active':
        todos = Todo.objects.filter(completed=False)
    elif filter_type == 'completed':
        todos = Todo.objects.filter(completed=True)
    else:
        todos = Todo.objects.all()

    return render(
        request,
        'examples/todomvc.html',
        {
            'todos': todos,
            'filter': filter_type,
            'total_count': Todo.objects.count(),
            'active_count': Todo.objects.filter(completed=False).count(),
            'completed_count': Todo.objects.filter(completed=True).count(),
        },
    )


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
            mode=consts.ElementPatchMode.APPEND,
        )


@datastar_response
def todomvc_toggle_view(request):
    todo_id = request.POST.get('id')
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.completed = not todo.completed
    todo.save()

    html = render_to_string('examples/fragments/todo_item.html', {'todo': todo})
    yield SSE.patch_elements(html, selector=f'#todo-{todo_id}')


@datastar_response
def todomvc_delete_view(request):
    todo_id = request.POST.get('id')
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.delete()

    yield SSE.remove_elements(selector=f'#todo-{todo_id}')


@datastar_response
def todomvc_clear_view(request):
    Todo.objects.filter(completed=True).delete()

    todos = Todo.objects.all()
    html = render_to_string('examples/fragments/todo_list.html', {'todos': todos})
    yield SSE.patch_elements(html, selector='#todo-list')


# ============================================================================
# 6. Inline Validation
# ============================================================================


class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    username = forms.CharField(min_length=3, max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


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
    page = int(request.GET.get('page', 1))
    items_per_page = 6
    contacts = Contact.objects.all()[
        (page - 1) * items_per_page : page * items_per_page
    ]
    has_more = Contact.objects.count() > page * items_per_page

    return render(
        request,
        'examples/infinite_scroll.html',
        {'contacts': contacts, 'page': page, 'has_more': has_more},
    )


@datastar_response
def infinite_scroll_load_view(request):
    page = int(request.GET.get('page', 1))
    items_per_page = 6
    contacts = Contact.objects.all()[
        (page - 1) * items_per_page : page * items_per_page
    ]
    has_more = Contact.objects.count() > page * items_per_page

    html = render_to_string(
        'examples/fragments/contact_list.html',
        {'contacts': contacts, 'page': page, 'has_more': has_more},
    )
    yield SSE.patch_elements(
        html, selector='#contact-list', mode=consts.ElementPatchMode.APPEND
    )


# ============================================================================
# 8. Lazy Tabs
# ============================================================================


def lazy_tabs_view(request):
    return render(request, 'examples/lazy_tabs.html', {'tab': 'home'})


@datastar_response
def lazy_tabs_tab_view(request):
    tab = request.GET.get('tab', 'home')
    content = {
        'home': 'Welcome to the home tab! This content was loaded lazily.',
        'about': 'About Us: We build modern web applications with Django and Datastar.',
        'contact': 'Contact us at: hello@example.com',
    }.get(tab, 'Content not found')

    html = render_to_string(
        'examples/fragments/tab_content.html', {'tab': tab, 'content': content}
    )
    yield SSE.patch_elements(html, selector='#tab-content')


# ============================================================================
# 9. File Upload
# ============================================================================


def file_upload_view(request):
    return render(request, 'examples/file_upload.html')


@datastar_response
def file_upload_upload_view(request):
    uploaded_file = request.FILES.get('file')

    if uploaded_file:
        result = f'Uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)'
    else:
        result = 'No file uploaded'

    html = render_to_string('examples/fragments/upload_result.html', {'result': result})
    yield SSE.patch_elements(html, selector='#upload-result')


# ============================================================================
# 10. Sortable
# ============================================================================


def sortable_view(request):
    items = Item.objects.all()
    return render(request, 'examples/sortable.html', {'items': items})


@datastar_response
def sortable_reorder_view(request):
    item_ids = request.POST.getlist('ids[]')

    for index, item_id in enumerate(item_ids):
        Item.objects.filter(pk=item_id).update(order=index)

    yield HttpResponse('Reordered')


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
