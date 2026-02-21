from django.urls import path

from . import views

app_name = 'examples'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('active-search/', views.active_search_view, name='active-search'),
    path('click-to-load/', views.click_to_load_view, name='click-to-load'),
    path('edit-row/', views.edit_row_view, name='edit-row'),
    path('contact-update/', views.contact_update_view, name='contact-update'),
    path('delete-row/', views.delete_row_view, name='delete-row'),
    path('todo-mvc/', views.todomvc_view, name='todo-mvc'),
    path('todo-mvc/toggle/', views.todomvc_toggle_view, name='todo-mvc-toggle'),
    path('todo-mvc/delete/', views.todomvc_delete_view, name='todo-mvc-delete'),
    path('todo-mvc/add/', views.todomvc_add_view, name='todo-mvc-add'),
    path('todo-mvc/clear/', views.todomvc_clear_view, name='todo-mvc-clear'),
    path('todo-mvc/filter/', views.todomvc_filter_view, name='todo-mvc-filter'),
    path('contact/', views.get_contact_view, name='get-contact'),
    path('inline-validation/', views.inline_validation_view, name='inline-validation'),
    path(
        'inline-validation/validate/',
        views.inline_validation_validate_view,
        name='inline-validation-validate',
    ),
    path('infinite-scroll/', views.infinite_scroll_view, name='infinite-scroll'),
    path('lazy-tabs/', views.lazy_tabs_view, name='lazy-tabs'),
    path('file-upload/', views.file_upload_view, name='file-upload'),
    path('file-processing/', views.file_processing_view, name='file-processing'),
    path(
        'file-processing-api/',
        views.file_processing_api_view,
        name='file-processing-api',
    ),
    path('sortable/', views.sortable_view, name='sortable'),
    path('notifications/', views.notifications_view, name='notifications'),
    path(
        'notifications/count/',
        views.notifications_count_view,
        name='notifications-count',
    ),
    path(
        'notifications/mark-read/',
        views.notifications_mark_read_view,
        name='notifications-mark-read',
    ),
    path('notifications/sse/', views.notifications_sse_view, name='notifications-sse'),
    path('bulk-update/', views.bulk_update_view, name='bulk-update'),
    path(
        'bulk-update/update/', views.bulk_update_update_view, name='bulk-update-update'
    ),
    # Search
    path('search/', views.search_view, name='search'),
    path('search/instant/', views.search_instant_view, name='search-instant'),
    # system messages
    path('system-messages/', views.system_messages_view, name='system-messages'),
    path(
        'system-messages/emit/',
        views.system_messages_emit_view,
        name='system-messages-emit',
    ),
]
