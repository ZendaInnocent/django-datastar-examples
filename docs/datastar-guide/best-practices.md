# Best Practices

## 1. Always Read Signals (Except Forms)

```python
# ✅ GOOD - Read signals for JSON-based requests
@datastar_response
def my_view(request):
    signals = read_signals(request)
    # Process signals...

# ✅ GOOD - Forms use request.POST directly
@datastar_response
def form_submit(request):
    name = request.POST.get('name')  # No read_signals needed
    # Process form data...

# ❌ BAD - Reading signals for form data
@datastar_response
def form_submit(request):
    signals = read_signals(request)
    name = signals.get('name')  # Wrong for forms
```

**Rule:** Use `read_signals()` only for JSON-based requests (default `contentType: 'json'`). For forms with `contentType: 'form'`, access data via `request.POST` and `request.FILES`.

## 2. Use Partial Templates

```python
# ✅ GOOD - Partial template
html = render_to_string('partials/item.html', {'item': item})
yield SSE.patch_elements(html, selector='#items')

# ❌ BAD - Inline HTML
yield SSE.patch_elements(f'<div>{item.name}</div>', selector='#items')
```

## 3. Handle Errors Gracefully

```python
@datastar_response
def my_view(request):
    signals = read_signals(request)

    try:
        # Business logic
        item = get_object_or_404(Item, id=signals['id'])
        html = render_to_string('partials/item.html', {'item': item})
        yield SSE.patch_elements(html, selector='#item-detail')
        yield SSE.patch_signals({'loading': False, 'error': None})

    except Exception as e:
        # Error handling
        error_html = render_to_string('partials/error.html', {'message': str(e)})
        yield SSE.patch_elements(error_html, selector='#error-container')
        yield SSE.patch_signals({'loading': False, 'error': str(e)})
```

## 4. Use Loading States

```html
<!-- ✅ GOOD - Loading indicators -->
<button
  data-on:click="@get('/api/data')"
  data-indicator:loading
  data-attr:disabled="$loading">
  <span data-show="!$loading">Load</span>
  <span data-show="$loading">Loading...</span>
</button>
```

## 5. Use `contentType: 'form'` for Form Submissions

```html
<!-- ✅ GOOD - Form with contentType: 'form' -->
<form data-on:submit="@post('/submit', {contentType: 'form'})">
  <input
    name="username"
    required />
  <button type="submit">Submit</button>
</form>

<!-- ❌ BAD - Form without contentType (sends signals instead) -->
<form data-on:submit="@post('/submit')">
  <input data-bind:username />
  <button type="submit">Submit</button>
</form>
```

```python
# ✅ GOOD - Django view handles form data
@datastar_response
def form_submit(request):
    username = request.POST.get('username')  # From form data
    # Process...

# ❌ BAD - Reading signals for form data
@datastar_response
def form_submit(request):
    signals = read_signals(request)
    username = signals.get('username')  # Wrong approach for forms
```

**Key Rules:**

- Always use `{contentType: 'form'}` for form submissions
- Use `name` attributes on form inputs (not `data-bind`)
- Access form data via `request.POST` and `request.FILES` in Django
- Use `enctype="multipart/form-data"` for file uploads
- Include `{% csrf_token %}` in forms

## 6. Data Security

```python
# ✅ GOOD - Implement proper access control
@datastar_response
def get_items(request):
    signals = read_signals(request)
    if not request.user.has_perm('core.view_item'):
        return SSE.patch_signals({'error': 'Permission denied'}, selector='#error')
    items = Item.objects.filter(user=request.user)  # User-specific filtering
    # ...

# ❌ BAD - No access control
@datastar_response
def get_items(request):
    items = Item.objects.all()  # Security issue!
```

## 7. Debounce Input Events

```html
<!-- ✅ GOOD - Debounced search -->
<input
  type="text"
  data-on:input__debounce.300ms="@get('/search')"
  data-bind:query />

<!-- ❌ BAD - No debounce -->
<input
  type="text"
  data-on:input="@get('/search')" />
# Too many requests
```

## 8. Throttle Polling

```html
<!-- ✅ GOOD - Throttled polling (min 5s) -->
<div data-on-interval__duration.5s="refreshData()"></div>

<!-- ❌ BAD - Too frequent -->
<div data-on-interval__duration.1s="refreshData()"></div>
```

## 9. Use Selectors Effectively

```python
# ✅ GOOD - Specific selector
yield SSE.patch_elements(html, selector='#item-123')

# ❌ BAD - Too broad
yield SSE.patch_elements(html, selector='div')
```

## 10. Preserve User State

```html
<!-- ✅ GOOD - Preserve form state -->
<input
  data-bind:username
  value="{{ initial_value }}" />
<div data-preserve-attr="checked">
  <input type="checkbox" />
</div>
```

## 11. Test View Responses

```python
# ✅ GOOD - Test SSE responses
@pytest.mark.asyncio
async def test_tour_update_view(client, tour):
    response = await client.post(f'/tours/{tour.id}/update', data={
        'title': 'Updated Tour'
    })
    assert response.status_code == 200
    assert b'datastar-patch-elements' in response.content

# ✅ GOOD - Test form submissions with contentType: 'form'
@pytest.mark.asyncio
async def test_booking_form_submission(client, tour):
    response = await client.post('/bookings/create', data={
        'tour_id': tour.id,
        'date': '2026-01-15',
        'participants': '2'
    })
    assert response.status_code == 200
    assert b'datastar-patch-signals' in response.content
```

---
