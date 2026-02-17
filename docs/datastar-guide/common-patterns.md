# Common Patterns

## Pattern 1: Modal Dialogs

```html
<!-- Open modal -->
<button data-on:click="$showModal = true">Open</button>

<!-- Modal -->
<div
  id="modal"
  data-show="$showModal"
  data-on:click__outside="$showModal = false">
  <div
    class="modal-content"
    data-on:click__stop>
    <h2>Title</h2>
    <p>Content</p>
    <button data-on:click="$showModal = false">Close</button>
  </div>
</div>
```

## Pattern 2: Confirm Actions

```html
<div data-signals="{confirmDelete: false, itemToDelete: null}">
  <!-- Delete button -->
  <button data-on:click="$itemToDelete = {{ item.id }}; $confirmDelete = true">
    Delete
  </button>

  <!-- Confirmation dialog -->
  <div data-show="$confirmDelete">
    <p>Are you sure you want to delete this item?</p>
    <form data-on:submit="@post('/items/delete', {contentType: 'form'})">
      <input
        type="hidden"
        name="item_id"
        data-bind:itemToDelete />
      <button type="submit">Yes, delete it</button>
    </form>
    <button data-on:click="$confirmDelete = false">Cancel</button>
  </div>
</div>
```

```python
@datastar_response
def item_delete(request):
    """
    Handle form-based delete action.
    Item ID extracted from form data.
    """
    item_id = request.POST.get('item_id')

    item = get_object_or_404(Item, id=item_id, business=request.user.business)
    item.delete()

    yield SSE.remove_elements(selector=f'#item-{item_id}')
    yield SSE.patch_signals({'confirmDelete': False, 'itemToDelete': None})
```

## Pattern 3: Live Search with Results

```html
<div data-signals="{query: '', results: [], selectedIndex: -1}">
  <input
    type="text"
    data-bind:query
    data-on:input__debounce.300ms="@get('/search')"
    data-on:keydown.up="$selectedIndex = Math.max(0, $selectedIndex - 1)"
    data-on:keydown.down="$selectedIndex = Math.min($results.length - 1, $selectedIndex + 1)"
    data-on:keydown.enter__prevent="selectResult($selectedIndex)" />

  <div
    id="results"
    data-show="$results.length">
    {% for result in results %}
    <div
      data-show="$selectedIndex === {{ forloop.counter0 }}"
      data-class:selected="$selectedIndex === {{ forloop.counter0 }}">
      {{ result.name }}
    </div>
    {% endfor %}
  </div>
</div>
```

## Pattern 4: Toggle Switches

```html
<div data-signals="{notificationsEnabled: true}">
  <form data-on:submit="@post('/settings/update', {contentType: 'form'})">
    <label class="toggle">
      <input
        type="checkbox"
        name="notifications_enabled"
        checked="checked"
        value="true"
        data-bind:notificationsEnabled
        data-on:change="this.closest('form').requestSubmit()" />
      <span class="toggle-slider"></span>
      <span>Notifications</span>
    </label>
  </form>
</div>
```

## Pattern 5: File Upload with Preview

```html
<div data-signals="{imagePreview: null, uploading: false}">
  <form
    id="image-upload-form"
    enctype="multipart/form-data"
    data-on:submit="@post('/upload/image', {contentType: 'form'})">
    <input
      type="file"
      name="image"
      accept="image/*"
      required
      data-on:change="showPreview(event); this.closest('form').requestSubmit()" />
  </form>

  <!-- Client-side preview -->
  <img
    id="preview-img"
    data-attr:src="$imagePreview"
    data-show="$imagePreview"
    class="preview" />

  <div data-show="$uploading">Uploading...</div>

  <script>
    function showPreview(evt) {
      const file = evt.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          document.getElementById('preview-img').src = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }
  </script>
</div>
```

```python
@datastar_response
def upload_image(request):
    """
    Handle multipart/form-data file upload.
    File accessed via request.FILES.
    """
    uploaded_file = request.FILES.get('image')

    if not uploaded_file:
        raise ValidationError({'image': 'No file uploaded'})

    # Save file to model
    item = Item.objects.create(
        business=request.user.business,
        image=uploaded_file
    )

    # Return uploaded image URL
    image_url = item.image.url

    yield SSE.patch_signals({
        'uploading': False,
        'imagePreview': image_url,
        'imageId': item.id
    })
```

## Pattern 6: Real-Time Notifications

```html
<div data-signals="{notifications: [], unreadCount: 0}">
  <button data-on:click="$showNotifications = true">
    Notifications
    <span
      class="badge"
      data-text="$unreadCount"
      data-show="$unreadCount"></span>
  </button>

  <div data-show="$showNotifications">
    <div id="notifications-list">
      {% for notification in notifications %}
      <div
        class="notification"
        data-class:unread="!notification.read">
        {{ notification.message }}
        <span class="time">{{ notification.time }}</span>
      </div>
      {% endfor %}
    </div>
  </div>

  <!-- Check for new notifications -->
  <div
    data-on-interval__duration.60s
    data-init="@get('/notifications/check')"></div>
</div>
```

```python
@datastar_response
def check_notifications(request):
    notifications = Notification.objects.filter(
        business=request.user.business,
        read=False
    ).order_by('-created_at')[:5]

    # Mark as read
    notifications.update(read=True)

    context = {'notifications': notifications}
    html = render_to_string('partials/notifications.html', context)
    yield SSE.patch_elements(html, selector='#notifications-list')
    yield SSE.patch_signals({
        'notifications': [
            {
                'id': n.id,
                'message': n.message,
                'time': n.created_at.strftime('%H:%M'),
                'read': n.read
            }
            for n in notifications
        ],
        'unreadCount': Notification.objects.filter(
            business=request.user.business,
            read=False
        ).count()
    })
```

---
