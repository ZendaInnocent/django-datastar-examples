"""
HowTo Configuration - Step-by-Step Guides for Datastar Examples

This module provides comprehensive, friendly instructions for building
each Datastar example in Django. Each guide includes:
- Clear step-by-step instructions
- Actual code extracted from working implementations
- Best practices and tips
"""

import inspect
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from django.urls import reverse

from examples import views


# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class HowToStep:
    """Represents a single step in the HowTo guide."""

    title: str
    description: str
    code: str
    language: str = 'python'  # python, html, django, javascript


@dataclass
class HowToExample:
    """Configuration for a single example's HowTo panel."""

    slug: str
    title: str
    description: str
    steps: list[HowToStep] = field(default_factory=list)
    doc_links: list[dict] = field(default_factory=list)

    # Internal - view functions
    _view_funcs: list[Callable] = field(default_factory=list, repr=False)
    _url_names: list[str] = field(default_factory=list, repr=False)
    _template_path: str = ''


# ============================================================================
# Helper Functions
# ============================================================================


def extract_view_code(view_func: Callable) -> str:
    """Extract the source code of a view function, cleaned for display."""
    try:
        source = inspect.getsource(view_func)
        # Clean up the source
        lines = source.split('\n')
        # Remove first line (def ...)
        if lines:
            lines = lines[1:]
        # Remove indentation
        if lines:
            # Find minimum indentation
            min_indent = float('inf')
            for line in lines:
                if line.strip():
                    indent = len(line) - len(line.lstrip())
                    min_indent = min(min_indent, indent)

            # Remove common indentation
            cleaned = []
            for line in lines:
                if line.strip():
                    cleaned.append(
                        line[min_indent:] if min_indent < float('inf') else line
                    )
                else:
                    cleaned.append('')

            return '\n'.join(cleaned)
        return source
    except (TypeError, OSError):
        return '# Code not available'


def get_url_pattern(url_name: str) -> str:
    """Get the URL pattern for a named URL."""
    try:
        return reverse(f'examples:{url_name}')
    except Exception:
        return f'/{url_name}/'


def extract_template_code(template_path: str, max_lines: int = 20) -> str:
    """Extract code from a template file."""
    try:
        # Try multiple base paths
        base_paths = [
            Path('templates'),
            Path('examples/templates'),
        ]

        for base in base_paths:
            full_path = base / template_path
            if full_path.exists():
                with open(full_path, encoding='utf-8') as f:
                    lines = f.readlines()[:max_lines]
                return ''.join(lines)
    except Exception:
        pass
    return '# Template not available'


# ============================================================================
# Active Search Example
# ============================================================================


def build_active_search_steps() -> list[HowToStep]:
    """Build comprehensive steps for Active Search example."""
    return [
        HowToStep(
            title='1. The View (Backend)',
            description='Create a view that handles both regular page loads and Datastar requests. Use read_signals() to read the search query from the frontend:',
            code=extract_view_code(views.active_search_view),
            language='python',
        ),
        HowToStep(
            title='2. The URLs',
            description='Add routes for the main view. The same view handles both page render and Datastar requests:',
            code="""path('active-search/', views.active_search_view, name='active-search'),""",
            language='python',
        ),
        HowToStep(
            title='3. The Template (Frontend)',
            description='Use data-bind to connect the input to a signal, and data-on with debounce to trigger searches after the user stops typing:',
            code="""<input
  type="text"
  placeholder="Search contacts..."
  data-bind:search
  data-on:input__debounce.200ms="@get('{% url 'examples:active-search' %}')"
/>""",
            language='html',
        ),
        HowToStep(
            title='4. The Fragment (Partial HTML)',
            description='Return an HTML fragment that Datastar merges into the DOM. Important: Use fragment IDs that match for proper merging:',
            code="""<div id="contact-list">
  {% for contact in contacts %}
  <div id="contact-{{ contact.pk }}">
    {{ contact.first_name }} {{ contact.last_name }}
  </div>
  {% endfor %}
</div>""",
            language='html',
        ),
        HowToStep(
            title='Key Concepts',
            description='Signals are the heart of Datastar. They store reactive data that automatically updates the UI when changed. Debouncing prevents excessive server requests while the user is typing.',
            code="""# Key Datastar concepts:
# 1. data-bind:SIGNAL_NAME - binds input to a signal
# 2. data-on:EVENT__debounce.MS - delays events to reduce server load
# 3. @get('/url/') - makes a GET request and merges response
# 4. Fragment IDs - Datastar uses HTML id attributes to merge updates""",
            language='python',
        ),
    ]


# ============================================================================
# Click to Load Example
# ============================================================================


def build_click_to_load_steps() -> list[HowToStep]:
    """Build comprehensive steps for Click to Load example."""
    return [
        HowToStep(
            title='1. The View (Backend)',
            description='Create a paginated view that returns SSE with append mode. Check for Datastar-Request header to return partial HTML:',
            code=extract_view_code(views.click_to_load_view),
            language='python',
        ),
        HowToStep(
            title='2. The URLs',
            description='Add routes for the main view. The same endpoint handles both initial load and pagination:',
            code="""path('click-to-load/', views.click_to_load_view, name='click-to-load'),""",
            language='python',
        ),
        HowToStep(
            title='3. The Template (Signals)',
            description='Initialize signals to track the current page and whether there are more items:',
            code="""<div data-signals="{page: 1, hasMore: true}">
  <!-- Contact list will be rendered here -->
</div>""",
            language='html',
        ),
        HowToStep(
            title='4. The Load More Button',
            description='Use data-on:click to increment the page and fetch more data. The mode=APPEND adds new items to the existing list:',
            code="""<button
  data-show="$hasMore"
  data-on:click="$page=$page+1; @get('{% url "examples:click-to-load" %}');"
>
  Load More
</button>""",
            language='html',
        ),
        HowToStep(
            title='5. The Fragment',
            description='Render contacts as fragments with unique IDs. Datastar will append these to the existing list:',
            code="""{% for contact in contacts %}
<div id="contact-{{ contact.pk }}">
  {{ contact.first_name }} {{ contact.last_name }}
</div>
{% endfor %}""",
            language='html',
        ),
        HowToStep(
            title='Key Concepts',
            description='ElementPatchMode.APPEND adds new elements without replacing existing ones. Use data-show to conditionally display elements based on signal values.',
            code="""# From datastar_py import consts
from datastar_py import consts

# Use APPEND mode to add to existing content
SSE.patch_elements(html, selector='#contact-list', mode=consts.ElementPatchMode.APPEND)

# Use data-show for conditional rendering
data-show="$hasMore"  # Only shows when hasMore signal is true""",
            language='python',
        ),
    ]


# ============================================================================
# Edit Row Example
# ============================================================================


def build_edit_row_steps() -> list[HowToStep]:
    """Build comprehensive steps for Edit Row example."""
    return [
        HowToStep(
            title='1. The Main View',
            description='Create a view that displays the data in read mode by default:',
            code=extract_view_code(views.edit_row_view),
            language='python',
        ),
        HowToStep(
            title='2. The Update View',
            description='Create a view that handles POST requests to update data. Return patched HTML for the updated row:',
            code=extract_view_code(views.contact_update_view),
            language='python',
        ),
        HowToStep(
            title='3. The URLs',
            description='Add routes for the main view and the update endpoint:',
            code="""path('edit-row/', views.edit_row_view, name='edit-row'),
path('edit-row/update/', views.contact_update_view, name='edit-row-update'),""",
            language='python',
        ),
        HowToStep(
            title='4. The Template (Display Mode)',
            description='Show contact details with an Edit button that switches to edit mode:',
            code="""<div id="contact-{{ contact.pk }}">
  <span>{{ contact.first_name }} {{ contact.last_name }}</span>
  <button data-on:click="@post('{% url "examples:edit-row-update" %}', {
  contactId: {{ contact.pk }}})">
    Edit
  </button>
</div>""",
            language='html',
        ),
        HowToStep(
            title='5. The Edit Form Template',
            description='Return a form when edit mode is triggered. The form submits to the update endpoint:',
            code="""<form id="contact-{{ contact.pk }}">
  <input name="first_name" value="{{ contact.first_name }}" />
  <input name="last_name" value="{{ contact.last_name }}" />
  <button type="submit">Save</button>
</form>""",
            language='html',
        ),
        HowToStep(
            title='Key Concepts',
            description='Use @post() to send form data. The view returns patched HTML that replaces the existing row. Fragment IDs ensure the correct element is updated.',
            code="""# Use @post() for form submissions
data-on:click="@post('/update-url/', {contactId: 1})"

# Return patched HTML to replace the element
SSE.patch_elements(html, selector=f'#contact-{contact.pk}')""",
            language='python',
        ),
    ]


# ============================================================================
# Delete Row Example
# ============================================================================


def build_delete_row_steps() -> list[HowToStep]:
    """Build comprehensive steps for Delete Row example."""
    return [
        HowToStep(
            title='1. The View',
            description='Handle delete requests and return SSE remove directive:',
            code=extract_view_code(views.delete_row_view),
            language='python',
        ),
        HowToStep(
            title='2. The URL',
            description='Add route for the delete endpoint:',
            code="""path('delete-row/', views.delete_row_view, name='delete-row'),""",
            language='python',
        ),
        HowToStep(
            title='3. The Delete Button',
            description='Add a delete button that sends a POST request. Optionally use confirm() for confirmation:',
            code="""<button
  data-on:click="?')) @if (confirm('Delete this contactpost('{% url "examples:delete-row" %}', {contactId: {{ contact.pk }}})"
>
  Delete
</button>""",
            language='html',
        ),
        HowToStep(
            title='4. Remove Elements',
            description='Use SSE.remove_elements() to remove the row from the DOM with animation:',
            code="""from datastar_py.django import ServerSentEventGenerator as SSE

# Remove the element from DOM
SSE.remove_elements(selector=f'#contact-{contact_id}')""",
            language='python',
        ),
        HowToStep(
            title='Key Concepts',
            description='SSE.remove_elements() deletes matched elements from the DOM. Combine with confirm() for user confirmation before deletion.',
            code="""# Remove element with selector
SSE.remove_elements(selector='#contact-123')

# Can also remove multiple elements
SSE.remove_elements(selector='.selected-items')""",
            language='python',
        ),
    ]


# ============================================================================
# TodoMVC Example
# ============================================================================


def build_todomvc_steps() -> list[HowToStep]:
    """Build comprehensive steps for TodoMVC example."""
    return [
        HowToStep(
            title='1. The Model',
            description='Define a Todo model with ordering for drag-and-drop functionality:',
            code="""class Todo(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']""",
            language='python',
        ),
        HowToStep(
            title='2. Add Todo View',
            description='Create a view to add new todos. Use PREPEND mode to add new items at the top:',
            code=extract_view_code(views.todomvc_add_view),
            language='python',
        ),
        HowToStep(
            title='3. Toggle Todo View',
            description='Handle toggling todo completion. Update the signal counts:',
            code=extract_view_code(views.todomvc_toggle_view),
            language='python',
        ),
        HowToStep(
            title='4. Delete Todo View',
            description='Remove a todo and update the counts:',
            code=extract_view_code(views.todomvc_delete_view),
            language='python',
        ),
        HowToStep(
            title='5. Filter View',
            description='Filter todos by active/completed/all:',
            code=extract_view_code(views.todomvc_filter_view),
            language='python',
        ),
        HowToStep(
            title='6. The Template',
            description='Create a todo list with add form, filter buttons, and item display:',
            code="""<!-- Add Todo Form -->
<form data-on:submit="@post('{% url "examples:todomvc-add" %}')">
  <input name="title" placeholder="What needs to be done?" />
</form>

<!-- Filter Buttons -->
<button data-on:click="@post('{% url "examples:todomvc-filter" %}', {filter: 'all'})">All</button>
<button data-on:click="@post('{% url "examples:todomvc-filter" %}', {filter: 'active'})">Active</button>
<button data-on:click="@post('{% url "examples:todomvc-filter" %}', {filter: 'completed'})">Completed</button>

<!-- Todo Items -->
<div id="todo-list">
  {% for todo in todos %}
  <div id="todo-{{ todo.pk }}">
    <input type="checkbox" {% if todo.is_completed %}checked{% endif %}
           data-on:change="@post('{% url "examples:todomvc-toggle" %}', {todoToggleId: {{ todo.pk }}})" />
    {{ todo.title }}
    <button data-on:click="@post('{% url "examples:todomvc-delete" %}', {todoToggleId: {{ todo.pk }}})">X</button>
  </div>
  {% endfor %}
</div>""",
            language='html',
        ),
        HowToStep(
            title='Key Concepts',
            description='Use data-on:change to trigger actions when checkboxes change. Update signal counts to reflect the current state.',
            code="""# Use PREPEND to add new items at the top
SSE.patch_elements(html, selector='#todo-list', mode=consts.ElementPatchMode.PREPEND)

# Use REMOVE to hide completed items when filtering
mode = consts.ElementPatchMode.REMOVE  # When filtering to 'active'

# Update multiple signals at once
SSE.patch_signals({
    'activeCount': counts.get('active'),
    'completedCount': counts.get('completed'),
})""",
            language='python',
        ),
    ]


# ============================================================================
# Inline Validation Example
# ============================================================================


def build_inline_validation_steps() -> list[HowToStep]:
    """Build comprehensive steps for Inline Validation example."""
    return [
        HowToStep(
            title='1. The Main View',
            description='Render the form with validation error containers:',
            code=extract_view_code(views.inline_validation_view),
            language='python',
        ),
        HowToStep(
            title='2. The Validation View',
            description='Create an endpoint that validates fields and returns error messages:',
            code=extract_view_code(views.inline_validation_validate_view),
            language='python',
        ),
        HowToStep(
            title='3. The URLs',
            description='Add routes for the form and validation endpoint:',
            code="""path('inline-validation/', views.inline_validation_view, name='inline-validation'),
path('inline-validation/validate/', views.inline_validation_validate_view, name='inline-validation-validate'),""",
            language='python',
        ),
        HowToStep(
            title='4. The Form Template',
            description='Bind form fields to signals and trigger validation on blur (when field loses focus):',
            code="""<form>
  <div>
    <label>Email</label>
    <input name="email" data-bind:email
           data-on:blur="@post('{% url "examples:inline-validation-validate" %}', {field: 'email'})" />
    <div id="email-error"></div>
  </div>

  <div>
    <label>Username</label>
    <input name="username" data-bind:username
           data-on:blur="@post('{% url "examples:inline-validation-validate" %}', {field: 'username'})" />
    <div id="username-error"></div>
  </div>
</form>""",
            language='html',
        ),
        HowToStep(
            title='5. The Error Fragment',
            description='Return error messages that get merged into error containers:',
            code="""{% if error %}
<span class="text-danger">{{ error }}</span>
{% else %}
<span class="text-success">OK</span>
{% endif %}""",
            language='html',
        ),
        HowToStep(
            title='Key Concepts',
            description='Use data-on:blur to trigger validation when a field loses focus. Return partial HTML that gets merged into error containers.',
            code="""# Validate field and return error HTML
errors = {}
if field == 'email':
    try:
        validate_email(value)
    except ValidationError:
        errors['email'] = 'Invalid email format'

# Patch error container
html = render_to_string('error_fragment.html', {'error': errors.get(field)})
SSE.patch_elements(html, selector=f'#{field}-error')""",
            language='python',
        ),
    ]


# ============================================================================
# Infinite Scroll Example
# ============================================================================


def build_infinite_scroll_steps() -> list[HowToStep]:
    """Build comprehensive steps for Infinite Scroll example."""
    return [
        HowToStep(
            title='1. The View',
            description='Create a paginated view that loads more items when page signal changes:',
            code=extract_view_code(views.infinite_scroll_view),
            language='python',
        ),
        HowToStep(
            title='2. The URL',
            description='Add route for the infinite scroll endpoint:',
            code="""path('infinite-scroll/', views.infinite_scroll_view, name='infinite-scroll'),""",
            language='python',
        ),
        HowToStep(
            title='3. The Template (Signals)',
            description='Initialize signals for page tracking and loading state:',
            code="""<div data-signals="{page: 1, hasMore: true, loading: false}">
  <div id="contact-list">
    <!-- Contacts rendered here -->
  </div>

  <!-- Infinite scroll trigger -->
  <div data-on:scroll="if (this.scrollTop + this.clientHeight >= this.scrollHeight) { $page = $page + 1; @get('{% url "examples:infinite-scroll" %}') }">
    Loading more...
  </div>
</div>""",
            language='html',
        ),
        HowToStep(
            title='4. The Scroll Detection',
            description='Use scroll event detection to trigger loading when user reaches bottom:',
            code="""<!-- Using Intersection Observer (more efficient) -->
<div id="sentinel"
     data-on:intersectionenter="$page=$page+1; @get('{% url "examples:infinite-scroll" %}')">
</div>

<!-- CSS for sentinel -->
<style>
#sentinel { height: 1px; }
</style>""",
            language='html',
        ),
        HowToStep(
            title='Key Concepts',
            description='Infinite scroll uses scroll events or Intersection Observer to detect when user reaches the end, then loads more data with APPEND mode.',
            code="""# Server returns hasMore signal to track if more data exists
SSE.patch_signals({'hasMore': page_obj.has_next()})

# Append new items to the list
SSE.patch_elements(html, selector='#contact-list',
                   mode=consts.ElementPatchMode.APPEND)""",
            language='python',
        ),
    ]


# ============================================================================
# Lazy Tabs Example
# ============================================================================


def build_lazy_tabs_steps() -> list[HowToStep]:
    """Build comprehensive steps for Lazy Tabs example."""
    return [
        HowToStep(
            title='1. The View',
            description='Return tab content on demand based on the activeTab signal:',
            code=extract_view_code(views.lazy_tabs_view),
            language='python',
        ),
        HowToStep(
            title='2. The URL',
            description='Add route for the lazy tabs endpoint:',
            code="""path('lazy-tabs/', views.lazy_tabs_view, name='lazy-tabs'),""",
            language='python',
        ),
        HowToStep(
            title='3. The Template',
            description='Create tab buttons that update the activeTab signal and fetch content:',
            code="""<!-- Tab Buttons -->
<button data-on:click="@post('{% url "examples:lazy-tabs" %}', {activeTab: 'home'})"
        data-class="$activeTab === 'home' ? 'active' : ''">
  Home
</button>

<button data-on:click="@post('{% url "examples:lazy-tabs" %}', {activeTab: 'about'})"
        data-class="$activeTab === 'about' ? 'active' : ''">
  About
</button>

<button data-on:click="@post('{% url "examples:lazy-tabs" %}', {activeTab: 'contact'})"
        data-class="$activeTab === 'contact' ? 'active' : ''">
  Contact
</button>

<!-- Tab Content Area -->
<div id="tab-content">
  <!-- Content loaded here -->
</div>""",
            language='html',
        ),
        HowToStep(
            title='4. The Content Fragment',
            description='Return HTML that replaces the tab content area:',
            code="""<div id="tab-content">
  {{ content }}
</div>""",
            language='html',
        ),
        HowToStep(
            title='Key Concepts',
            description='Tabs work by sending the selected tab ID to the server, which returns the appropriate content. Use data-class for conditional active styling.',
            code="""# Server receives activeTab signal and returns content
signals = read_signals(request)
tab = signals.get('activeTab', 'home')

content = {'home': '...', 'about': '...', 'contact': '...'}.get(tab)

# Update both content and signal
SSE.patch_elements(html, selector='#tab-content')
SSE.patch_signals({'activeTab': tab})""",
            language='python',
        ),
    ]


# ============================================================================
# File Upload Example
# ============================================================================


def build_file_upload_steps() -> list[HowToStep]:
    """Build comprehensive steps for File Upload example."""
    return [
        HowToStep(
            title='1. The View',
            description='Handle file upload via POST request:',
            code=extract_view_code(views.file_upload_view),
            language='python',
        ),
        HowToStep(
            title='2. The URL',
            description='Add route for the file upload endpoint:',
            code="""path('file-upload/', views.file_upload_view, name='file-upload'),""",
            language='python',
        ),
        HowToStep(
            title='3. The Upload Form',
            description='Use data-on:change to trigger upload when file is selected:',
            code="""<form method="post" enctype="multipart/form-data">
  {% csrf_token %}
  <input type="file" name="file"
         data-on:change="@post('{% url "examples:file-upload" %}')" />
</form>

<div id="upload-result">
  <!-- Upload result appears here -->
</div>""",
            language='html',
        ),
        HowToStep(
            title='4. Handling Files',
            description='Access uploaded files via request.FILES:',
            code="""if request.method == 'POST':
    uploaded_file = request.FILES.get('file')
    if uploaded_file:
        # Process the file
        filename = uploaded_file.name
        size = uploaded_file.size
        content = uploaded_file.read()""",
            language='python',
        ),
        HowToStep(
            title='Key Concepts',
            description='File uploads work like regular forms with enctype="multipart/form-data". Use data-on:change to auto-submit when file is selected.',
            code="""# Handle file upload
uploaded_file = request.FILES.get('file')

# Return result HTML
html = render_to_string('upload_result.html', {'result': 'Uploaded: ...'})
SSE.patch_elements(html, selector='#upload-result')""",
            language='python',
        ),
    ]


# ============================================================================
# Sortable Example
# ============================================================================


def build_sortable_steps() -> list[HowToStep]:
    """Build comprehensive steps for Sortable (Drag and Drop) example."""
    return [
        HowToStep(
            title='1. The View',
            description='Handle reorder POST and update the database:',
            code=extract_view_code(views.sortable_view),
            language='python',
        ),
        HowToStep(
            title='2. The URL',
            description='Add route for the sortable endpoint:',
            code="""path('sortable/', views.sortable_view, name='sortable'),""",
            language='python',
        ),
        HowToStep(
            title='3. The Template',
            description='Use HTML5 drag and drop or a library. Send new order on drop:',
            code="""<!-- Draggable items -->
<ul id="sortable-list">
  {% for item in items %}
  <li id="item-{{ item.pk }}" draggable="true"
      data-id="{{ item.pk }}">
    {{ item.name }}
  </li>
  {% endfor %}
</ul>

<!-- Use SortableJS or similar library -->
<script>
  new Sortable(listElement, {
    onEnd: function (evt) {
      // Get new order and send to server
      const order = [...listElement.children].map(el => el.dataset.id);
      datastar.post('/sortable/', {order: order});
    }
  });
</script>""",
            language='html',
        ),
        HowToStep(
            title='4. Bulk Update',
            description='Use bulk_update to efficiently update multiple records:',
            code="""# Update all items with new order
new_ordered_items = []
for index, item_pk in enumerate(current_order, start=1):
    item = Item.objects.get(pk=item_pk)
    item.order = index
    new_ordered_items.append(item)

Item.objects.bulk_update(new_ordered_items, fields=['order'])""",
            language='python',
        ),
        HowToStep(
            title='Key Concepts',
            description='Drag and drop requires JavaScript library integration. Send the new order array to server and use bulk_update for efficiency.',
            code="""# Return updated signals
SSE.patch_signals({'order': current_order})

# Use bulk_update for efficiency (single query)
Item.objects.bulk_update(items, fields=['order'])""",
            language='python',
        ),
    ]


# ============================================================================
# Notifications Example
# ============================================================================


def build_notifications_steps() -> list[HowToStep]:
    """Build comprehensive steps for Notifications example."""
    return [
        HowToStep(
            title='1. The SSE View',
            description='Create a view that streams notifications using Server-Sent Events:',
            code=extract_view_code(views.notifications_sse_view),
            language='python',
        ),
        HowToStep(
            title='2. Mark as Read View',
            description='Handle marking notifications as read:',
            code=extract_view_code(views.notifications_mark_read_view),
            language='python',
        ),
        HowToStep(
            title='3. The URLs',
            description='Add routes for notifications:',
            code="""path('notifications/', views.notifications_view, name='notifications'),
path('notifications/sse/', views.notifications_sse_view, name='notifications-sse'),
path('notifications/mark-read/', views.notifications_mark_read_view, name='notifications-mark-read'),""",
            language='python',
        ),
        HowToStep(
            title='4. The Template',
            description='Connect to SSE stream and display notifications:',
            code="""<!-- SSE Connection -->
<div data-store="{notifications: [], notificationCount: 0}"
     data-on:load="@connect('{% url "examples:notifications-sse" %}')">

  <!-- Notification Badge -->
  <span data-show="$notificationCount > 0">
    {{ $notificationCount }} notifications
  </span>

  <!-- Notifications List -->
  <div id="notifications-list">
    {% for notification in notifications %}
    <div id="notification-{{ notification.pk }}">
      {{ notification.message }}
    </div>
    {% endfor %}
  </div>
</div>""",
            language='html',
        ),
        HowToStep(
            title='5. SSE Generator',
            description='Stream notifications with delays between each:',
            code="""# Stream notifications with delay
for notification in notifications:
    alert = render_to_string('notification_alert.html', {...})

    SSE.patch_elements(alert, selector='#notifications-list',
                      mode=consts.ElementPatchMode.APPEND)

    time.sleep(3)  # Delay between notifications""",
            language='python',
        ),
        HowToStep(
            title='Key Concepts',
            description='SSE streams keep a persistent connection to push updates. Use @connect() to establish the stream and receive real-time updates.',
            code="""# Use @connect for SSE streams
data-on:load="@connect('/notifications/sse/')"

# SSE keeps connection open and streams events
for notification in notifications:
    yield SSE.patch_elements(html, selector='#notifications-list')
    time.sleep(2)  # Stream with delay""",
            language='python',
        ),
    ]


# ============================================================================
# Bulk Update Example
# ============================================================================


def build_bulk_update_steps() -> list[HowToStep]:
    """Build comprehensive steps for Bulk Update example."""
    return [
        HowToStep(
            title='1. The Main View',
            description='Display a table with checkboxes for selection:',
            code=extract_view_code(views.bulk_update_view),
            language='python',
        ),
        HowToStep(
            title='2. The Update View',
            description='Process bulk actions on selected items:',
            code=extract_view_code(views.bulk_update_update_view),
            language='python',
        ),
        HowToStep(
            title='3. The URLs',
            description='Add routes for bulk update:',
            code="""path('bulk-update/', views.bulk_update_view, name='bulk-update'),
path('bulk-update/update/', views.bulk_update_update_view, name='bulk-update-update'),""",
            language='python',
        ),
        HowToStep(
            title='4. The Template',
            description='Create checkboxes that collect selected IDs and action buttons:',
            code="""<form method="post" action="{% url 'examples:bulk-update-update' %}">
  {% csrf_token %}

  <table id="contact-table">
    {% for contact in contacts %}
    <tr id="contact-{{ contact.pk }}">
      <td>
        <input type="checkbox" name="selected_ids" value="{{ contact.pk }}" />
      </td>
      <td>{{ contact.name }}</td>
      <td>{{ contact.email }}</td>
    </tr>
    {% endfor %}
  </table>

  <button type="submit" name="action" value="activate">Activate Selected</button>
  <button type="submit" name="action" value="deactivate">Deactivate Selected</button>
</form>""",
            language='html',
        ),
        HowToStep(
            title='5. Handle Bulk Actions',
            description='Process selected IDs and perform bulk updates:',
            code="""selected_ids = request.POST.getlist('selected_ids')
action = request.POST.get('action')

if action == 'activate':
    updated_count = Contact.objects.filter(pk__in=selected_ids).update(
        is_active=True
    )

if action == 'deactivate':
    updated_count = Contact.objects.filter(pk__in=selected_ids).update(
        is_active=False
    )""",
            language='python',
        ),
        HowToStep(
            title='Key Concepts',
            description='Use getlist() to collect multiple checkbox values. Use QuerySet.update() for efficient bulk operations.',
            code="""# Bulk update - single query, no ORM overhead
Contact.objects.filter(pk__in=selected_ids).update(is_active=True)

# Return updated table
html = render_to_string('contact_table.html', {'contacts': contacts})
SSE.patch_elements(html, selector='#contact-table')""",
            language='python',
        ),
    ]


# ============================================================================
# System Messages Example
# ============================================================================


def build_system_messages_steps() -> list[HowToStep]:
    """Build comprehensive steps for System Messages example."""
    return [
        HowToStep(
            title='1. The View',
            description='Create a view that can emit different message types:',
            code=extract_view_code(views.system_messages_view),
            language='python',
        ),
        HowToStep(
            title='2. The Emit View',
            description='Generate messages and return them via SSE:',
            code=extract_view_code(views.system_messages_emit_view),
            language='python',
        ),
        HowToStep(
            title='3. The URLs',
            description='Add routes for system messages:',
            code="""path('system-messages/', views.system_messages_view, name='system-messages'),
path('system-messages/emit/', views.system_messages_emit_view, name='system-messages-emit'),""",
            language='python',
        ),
        HowToStep(
            title='4. The Template',
            description='Create buttons to trigger different message types:',
            code="""<!-- Message Display Area -->
<div id="messages-container">
  {% if messages %}
    {% for message in messages %}
    <div class="alert alert-{{ message.tags }}">
      {{ message }}
    </div>
    {% endfor %}
  {% endif %}
</div>

<!-- Trigger Buttons -->
<button data-on:click="@post('{% url "examples:system-messages-emit" %}', {level: 'success'})">
  Show Success
</button>

<button data-on:click="@post('{% url "examples:system-messages-emit" %}', {level: 'error'})">
  Show Error
</button>

<button data-on:click="@post('{% url "examples:system-messages-emit" %}', {level: 'warning'})">
  Show Warning
</button>""",
            language='html',
        ),
        HowToStep(
            title='5. Django Messages + Datastar',
            description='Use Django messages framework with Datastar response:',
            code="""# Use Django messages framework
from django.contrib import messages

def view(request):
    messages.success(request, 'Operation completed!')
    messages.error(request, 'Something went wrong.')
    messages.warning(request, 'Warning message.')
    messages.info(request, 'Info message.')

# Use DatastarWithMessagesResponse to auto-inject messages
from examples.utils import DatastarWithMessagesResponse

return DatastarWithMessagesResponse(request, SSE.patch_signals({...}))""",
            language='python',
        ),
        HowToStep(
            title='Key Concepts',
            description='Django messages integrate with Datastar through middleware that extracts messages and injects them into SSE responses.',
            code="""# DatastarWithMessagesResponse handles Django messages
from examples.utils import DatastarWithMessagesResponse

return DatastarWithMessagesResponse(
    request,
    SSE.patch_signals({'action': 'completed'})
)

# Messages are automatically injected into the response""",
            language='python',
        ),
    ]


# ============================================================================
# Build All Example Configurations
# ============================================================================


EXAMPLES: dict[str, HowToExample] = {
    'active-search': HowToExample(
        slug='active-search',
        title='Active Search',
        description='Search a contacts database as you type with debounced input',
        steps=build_active_search_steps(),
        doc_links=[
            {
                'title': 'Understanding Signals',
                'url': '/docs/datastar-guide/core-concepts.md#signals',
            },
            {
                'title': 'Debouncing Input Events',
                'url': '/docs/datastar-guide/best-practices.md#debounce-input-events',
            },
            {
                'title': 'Server-Sent Events (SSE)',
                'url': '/docs/datastar-guide/core-concepts.md#sse-events',
            },
        ],
    ),
    'click-to-load': HowToExample(
        slug='click-to-load',
        title='Click to Load',
        description='Load more content on demand with pagination',
        steps=build_click_to_load_steps(),
        doc_links=[
            {
                'title': 'Element Patch Modes',
                'url': '/docs/datastar-guide/core-concepts.md#element-patch-modes',
            },
            {
                'title': 'Click Events',
                'url': '/docs/datastar-guide/core-concepts.md#event-handling',
            },
        ],
    ),
    'edit-row': HowToExample(
        slug='edit-row',
        title='Edit Row',
        description='Inline editing of table rows with instant updates',
        steps=build_edit_row_steps(),
        doc_links=[
            {
                'title': 'Form Handling',
                'url': '/docs/datastar-guide/django-integration.md#forms',
            },
            {
                'title': 'POST Requests',
                'url': '/docs/datastar-guide/core-concepts.md#post-requests',
            },
        ],
    ),
    'delete-row': HowToExample(
        slug='delete-row',
        title='Delete Row',
        description='Remove rows with confirmation and animation',
        steps=build_delete_row_steps(),
        doc_links=[
            {
                'title': 'Remove Elements',
                'url': '/docs/datastar-guide/core-concepts.md#remove-elements',
            },
        ],
    ),
    'todo-mvc': HowToExample(
        slug='todo-mvc',
        title='TodoMVC',
        description='Full CRUD Todo application with localStorage persistence',
        steps=build_todomvc_steps(),
        doc_links=[
            {
                'title': 'Toggle Events',
                'url': '/docs/datastar-guide/core-concepts.md#toggle-events',
            },
            {
                'title': 'Conditional Rendering',
                'url': '/docs/datastar-guide/core-concepts.md#conditional-rendering',
            },
        ],
    ),
    'inline-validation': HowToExample(
        slug='inline-validation',
        title='Inline Validation',
        description='Real-time form validation with server-side feedback',
        steps=build_inline_validation_steps(),
        doc_links=[
            {
                'title': 'Validation Patterns',
                'url': '/docs/datastar-guide/best-practices.md#validation',
            },
            {
                'title': 'Blur Events',
                'url': '/docs/datastar-guide/core-concepts.md#blur-events',
            },
        ],
    ),
    'infinite-scroll': HowToExample(
        slug='infinite-scroll',
        title='Infinite Scroll',
        description='Lazy loading of content as user scrolls',
        steps=build_infinite_scroll_steps(),
        doc_links=[
            {
                'title': 'Scroll Events',
                'url': '/docs/datastar-guide/core-concepts.md#scroll-events',
            },
            {
                'title': 'Intersection Observer',
                'url': '/docs/datastar-guide/core-concepts.md#intersection-observer',
            },
        ],
    ),
    'lazy-tabs': HowToExample(
        slug='lazy-tabs',
        title='Lazy Tabs',
        description='Tab content loaded on demand',
        steps=build_lazy_tabs_steps(),
        doc_links=[
            {
                'title': 'Conditional Classes',
                'url': '/docs/datastar-guide/core-concepts.md#conditional-classes',
            },
        ],
    ),
    'file-upload': HowToExample(
        slug='file-upload',
        title='File Upload',
        description='Drag and drop file uploads with progress',
        steps=build_file_upload_steps(),
        doc_links=[
            {
                'title': 'File Uploads',
                'url': '/docs/datastar-guide/django-integration.md#file-uploads',
            },
            {
                'title': 'Change Events',
                'url': '/docs/datastar-guide/core-concepts.md#change-events',
            },
        ],
    ),
    'sortable': HowToExample(
        slug='sortable',
        title='Sortable',
        description='Drag and drop reordering with server sync',
        steps=build_sortable_steps(),
        doc_links=[
            {
                'title': 'Drag and Drop',
                'url': '/docs/datastar-guide/core-concepts.md#drag-and-drop',
            },
            {
                'title': 'Bulk Operations',
                'url': '/docs/datastar-guide/django-integration.md#bulk-operations',
            },
        ],
    ),
    'notifications': HowToExample(
        slug='notifications',
        title='Notifications',
        description='Real-time notifications with SSE updates',
        steps=build_notifications_steps(),
        doc_links=[
            {
                'title': 'Server-Sent Events',
                'url': '/docs/datastar-guide/core-concepts.md#sse-events',
            },
            {
                'title': 'SSE Connections',
                'url': '/docs/datastar-guide/core-concepts.md#sse-connections',
            },
        ],
    ),
    'bulk-update': HowToExample(
        slug='bulk-update',
        title='Bulk Update',
        description='Select and update multiple records at once',
        steps=build_bulk_update_steps(),
        doc_links=[
            {
                'title': 'Bulk Operations',
                'url': '/docs/datastar-guide/django-integration.md#bulk-operations',
            },
            {
                'title': 'Form Collections',
                'url': '/docs/datastar-guide/django-integration.md#forms',
            },
        ],
    ),
    'system-messages': HowToExample(
        slug='system-messages',
        title='System Messages',
        description='User feedback messages (success, error, info)',
        steps=build_system_messages_steps(),
        doc_links=[
            {
                'title': 'Django Messages',
                'url': '/docs/datastar-guide/django-integration.md#messages',
            },
        ],
    ),
}


# ============================================================================
# Helper Functions
# ============================================================================


def get_example(slug: str) -> Optional[HowToExample]:
    """Get HowTo configuration for an example by slug."""
    return EXAMPLES.get(slug)


def get_all_examples() -> list[HowToExample]:
    """Get all example configurations."""
    return list(EXAMPLES.values())


def refresh_example(slug: str) -> HowToExample:
    """Regenerate an example's steps from current code."""
    example = EXAMPLES.get(slug)
    if example and slug in BUILDERS:
        example.steps = BUILDERS[slug]()
    return example


# Map slugs to builder functions
BUILDERS = {
    'active-search': build_active_search_steps,
    'click-to-load': build_click_to_load_steps,
    'edit-row': build_edit_row_steps,
    'delete-row': build_delete_row_steps,
    'todo-mvc': build_todomvc_steps,
    'inline-validation': build_inline_validation_steps,
    'infinite-scroll': build_infinite_scroll_steps,
    'lazy-tabs': build_lazy_tabs_steps,
    'file-upload': build_file_upload_steps,
    'sortable': build_sortable_steps,
    'notifications': build_notifications_steps,
    'bulk-update': build_bulk_update_steps,
    'system-messages': build_system_messages_steps,
}
