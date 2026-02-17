from django.urls import path

from . import views

app_name = 'examples'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('active-search/', views.active_search_view, name='active-search'),
    path(
        'active-search/search/',
        views.active_search_search_view,
        name='active-search-search',
    ),
    path('click-to-load/', views.click_to_load_view, name='click-to-load'),
    path(
        'click-to-load/more/', views.click_to_load_more_view, name='click-to-load-more'
    ),
    path('edit-row/', views.edit_row_view, name='edit-row'),
    path('edit-row/update/', views.edit_row_update_view, name='edit-row-update'),
    path('delete-row/', views.delete_row_view, name='delete-row'),
    path('delete-row/remove/', views.delete_row_remove_view, name='delete-row-remove'),
    path('todo-mvc/', views.todomvc_view, name='todo-mvc'),
    path('todo-mvc/toggle/', views.todomvc_toggle_view, name='todo-mvc-toggle'),
    path('todo-mvc/delete/', views.todomvc_delete_view, name='todo-mvc-delete'),
    path('todo-mvc/add/', views.todomvc_add_view, name='todo-mvc-add'),
    path('todo-mvc/clear/', views.todomvc_clear_view, name='todo-mvc-clear'),
    path('inline-validation/', views.inline_validation_view, name='inline-validation'),
    path(
        'inline-validation/validate/',
        views.inline_validation_validate_view,
        name='inline-validation-validate',
    ),
    path('infinite-scroll/', views.infinite_scroll_view, name='infinite-scroll'),
    path(
        'infinite-scroll/load/',
        views.infinite_scroll_load_view,
        name='infinite-scroll-load',
    ),
    path('lazy-tabs/', views.lazy_tabs_view, name='lazy-tabs'),
    path('lazy-tabs/tab/', views.lazy_tabs_tab_view, name='lazy-tabs-tab'),
    path('file-upload/', views.file_upload_view, name='file-upload'),
    path(
        'file-upload/upload/', views.file_upload_upload_view, name='file-upload-upload'
    ),
    path('sortable/', views.sortable_view, name='sortable'),
    path('sortable/reorder/', views.sortable_reorder_view, name='sortable-reorder'),
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
    path('bulk-update/', views.bulk_update_view, name='bulk-update'),
    path(
        'bulk-update/update/', views.bulk_update_update_view, name='bulk-update-update'
    ),
]
