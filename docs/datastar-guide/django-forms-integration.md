# Django Forms Integration

When using Datastar with Django, always use `contentType: 'form'` for form submissions. This approach:

- Sends traditional form data via `request.POST` and `request.FILES`
- Works with Django's built-in form validation
- Supports file uploads with `multipart/form-data`
- Integrates seamlessly with Django Forms
- Respects form element `required` attributes

## HTML Form Pattern

```html
<form
  data-on:submit="@post('/submit', {contentType: 'form'})"
  data-indicator:loading>
  {% csrf_token %}

  <div class="form-group">
    <label for="username">Username</label>
    <input
      id="username"
      name="username"
      type="text"
      required />
  </div>

  <div class="form-group">
    <label for="email">Email</label>
    <input
      id="email"
      name="email"
      type="email"
      required />
  </div>

  <button
    type="submit"
    data-attr:disabled="$loading">
    <span data-show="!$loading">Submit</span>
    <span data-show="$loading">Submitting...</span>
  </button>
</form>
```

**Key Points:**

- Always include `{% csrf_token %}` for CSRF protection
- Use `name` attributes (not `data-bind`) for form fields
- Use `required` attribute for client-side validation
- Use `data-indicator:loading` for loading state

## Django Form Class Pattern

```python
# forms.py
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['client', 'tour', 'date', 'participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'participants': forms.NumberInput(attrs={'min': 1, 'max': 20}),
        }

    def __init__(self, *args, **kwargs):
        self.business = kwargs.pop('business', None)
        super().__init__(*args, **kwargs)

        # Filter choices by business
        if self.business:
            self.fields['client'].queryset = Client.objects.filter(
                business=self.business
            )
            self.fields['tour'].queryset = Tour.objects.filter(
                business=self.business
            )
```

```python
# views.py
@datastar_response
def booking_create(request: HttpRequest):
    """
    Create booking using Django Form.
    """
    form = BookingForm(request.POST, business=request.user.business)

    if form.is_valid():
        booking = form.save(commit=False)
        booking.business = request.user.business
        booking.status = 'pending'
        booking.save()

        # Success response
        context = {'booking': booking}
        html = render_to_string('partials/booking_success.html', context)
        yield SSE.patch_elements(html, selector='#booking-form-container')
        yield SSE.patch_signals({
            'loading': False,
            'success': True,
            'errors': {}
        })
    else:
        # Validation errors
        context = {'errors': form.errors}
        html = render_to_string('partials/form_errors.html', context)
        yield SSE.patch_elements(html, selector='#form-errors')
        yield SSE.patch_signals({
            'loading': False,
            'errors': form.errors
        })
```

## Manual Form Handling

```python
@datastar_response
def create_item(request: HttpRequest):
    """
    Handle form submission manually (without Django Form class).
    """
    # Extract form data
    name = request.POST.get('name')
    description = request.POST.get('description')
    price = request.POST.get('price')

    # Manual validation
    errors = {}
    if not name:
        errors['name'] = 'Name is required'
    if not price:
        errors['price'] = 'Price is required'
    else:
        try:
            price = float(price)
            if price < 0:
                errors['price'] = 'Price must be positive'
        except ValueError:
            errors['price'] = 'Price must be a number'

    if errors:
        # Return errors
        context = {'errors': errors}
        html = render_to_string('partials/form_errors.html', context)
        yield SSE.patch_elements(html, selector='#form-errors')
        yield SSE.patch_signals({'loading': False, 'errors': errors})
        return

    # Create item
    item = Item.objects.create(
        business=request.user.business,
        name=name,
        description=description,
        price=price
    )

    # Success
    context = {'item': item}
    html = render_to_string('partials/item.html', context)
    yield SSE.patch_elements(html, selector='#items-container', mode='prepend')
    yield SSE.patch_signals({
        'loading': False,
        'errors': {},
        'success': True
    })
```

## File Upload Pattern

```html
<form
  enctype="multipart/form-data"
  data-on:submit="@post('/upload', {contentType: 'form'})"
  data-indicator:uploading>
  {% csrf_token %}

  <div class="form-group">
    <label for="file">Upload File</label>
    <input
      id="file"
      name="file"
      type="file"
      required />
  </div>

  <button
    type="submit"
    data-attr:disabled="$uploading">
    <span data-show="!$uploading">Upload</span>
    <span data-show="$uploading">Uploading...</span>
  </button>
</form>
```

```python
@datastar_response
def upload_file(request: HttpRequest):
    """
    Handle multipart/form-data file upload.
    """
    uploaded_file = request.FILES.get('file')

    if not uploaded_file:
        errors = {'file': 'No file uploaded'}
        html = render_to_string('partials/form_errors.html', {'errors': errors})
        yield SSE.patch_elements(html, selector='#form-errors')
        yield SSE.patch_signals({'loading': False, 'errors': errors})
        return

    # Validate file
    if not uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        errors = {'file': 'Only image files are allowed'}
        html = render_to_string('partials/form_errors.html', {'errors': errors})
        yield SSE.patch_elements(html, selector='#form-errors')
        yield SSE.patch_signals({'loading': False, 'errors': errors})
        return

    # Save to model
    item = Item.objects.create(
        business=request.user.business,
        image=uploaded_file
    )

    # Return success with image URL
    context = {'image_url': item.image.url}
    html = render_to_string('partials/upload_success.html', context)
    yield SSE.patch_elements(html, selector='#upload-container')
    yield SSE.patch_signals({
        'loading': False,
        'errors': {},
        'imagePreview': item.image.url
    })
```

## Form Error Display

```html
<!-- Form errors container -->
<div
  id="form-errors"
  class="alert alert-danger"
  data-show="Object.keys($errors).length > 0">
  <!-- General error -->
  <div
    data-show="$errors.general"
    class="error-message">
    {{ errors.general }}
  </div>

  <!-- Field-specific errors -->
  <div data-on-signal-patch-filter="{include: /^[^general]/}">
    {% for field_name, error_list in errors.items() %} {% if field_name !=
    'general' %}
    <div class="field-error">
      <strong>{{ field_name|title }}:</strong>
      {% for error in error_list %} {{ error }} {% endfor %}
    </div>
    {% endif %} {% endfor %}
  </div>
</div>
```

## Form Reset Pattern

```python
@datastar_response
def form_submit(request: HttpRequest):
    """
    Process form and reset it on success.
    """
    form = MyForm(request.POST)

    if form.is_valid():
        form.save(commit=False).business = request.user.business
        form.save()

        # Clear form by replacing it
        html = render_to_string('partials/my_form.html')
        yield SSE.patch_elements(html, selector='#my-form')
        yield SSE.patch_signals({'loading': False, 'success': True})
    else:
        # Show errors
        html = render_to_string('partials/form_errors.html', {'errors': form.errors})
        yield SSE.patch_elements(html, selector='#form-errors')
        yield SSE.patch_signals({'loading': False})
```

---
