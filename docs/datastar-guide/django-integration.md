# Django Integration

## Basic View Pattern

```python
# tours/views.py
from datastar_py.django import datastar_response, read_signals, ServerSentEventGenerator as SSE
from django.shortcuts import render_to_string
from django.http import HttpRequest
import asyncio

@datastar_response
def tour_event_update(request: HttpRequest, event_id: int):
    """
    Update tour event with real-time feedback.
    """
    signals = read_signals(request)

    # Get the tour event
    tour_event = get_object_or_404(TourEvent, id=event_id, business=request.user.business)

    # Validate signals
    errors = {}
    if not signals.get('title'):
        errors['title'] = 'Title is required'

    if errors:
        error_html = render_to_string('partials/error_messages.html', {'errors': errors})
        yield SSE.patch_elements(error_html, selector='#errors')
        yield SSE.patch_signals({'loading': False})
        return

    # Update the event
    tour_event.title = signals.get('title')
    tour_event.save()

    # Render updated partial
    context = {'event': tour_event}
    html = render_to_string('partials/tour_event.html', context)
    yield SSE.patch_elements(html, selector='#event-detail')
    yield SSE.patch_signals({
        'loading': False,
        'success': True
    })
```

## Long-Lived Stream Pattern

```python
@datastar_response
async def live_booking_updates(request: HttpRequest):
    """
    Stream booking updates in real-time.
    """
    signals = read_signals(request)
    booking_id = signals.get('bookingId')

    while True:
        booking = await sync_to_async(Booking.objects.get)(
            id=booking_id,
            business=request.user.business
        )

        # Send status update
        context = {'booking': booking}
        html = await render_to_string('partials/booking_status.html', context)
        yield SSE.patch_elements(html, selector='#booking-status')

        # Update signals
        yield SSE.patch_signals({
            'status': booking.status,
            'progress': booking.progress_percentage
        })

        # Wait before next update
        await asyncio.sleep(2)

        # Break if booking is complete
        if booking.status == 'completed':
            break
```

## Form Submission Pattern

```python
from django.core.exceptions import ValidationError
from django.forms import ModelForm

@datastar_response
def booking_create(request: HttpRequest):
    """
    Handle form submission with contentType: 'form'.
    Form data accessed via request.POST and request.FILES.
    """
    try:
        # Extract form data
        client_id = request.POST.get('client_id')
        tour_id = request.POST.get('tour_id')
        date = request.POST.get('date')
        participants = request.POST.get('participants', '1')

        # Validate required fields
        if not client_id:
            raise ValidationError({'client_id': 'Client is required'})
        if not tour_id:
            raise ValidationError({'tour_id': 'Tour is required'})
        if not date:
            raise ValidationError({'date': 'Date is required'})

        # Get related objects
        client = get_object_or_404(Client, id=client_id, business=request.user.business)
        tour = get_object_or_404(Tour, id=tour_id, business=request.user.business)

        # Create booking
        booking = Booking.objects.create(
            business=request.user.business,
            client=client,
            tour=tour,
            date=date,
            participants=int(participants),
            status='pending'
        )

        # Success response
        success_html = render_to_string('partials/booking_success.html', {'booking': booking})
        yield SSE.patch_elements(success_html, selector='#booking-form-container')
        yield SSE.patch_signals({
            'loading': False,
            'showSuccess': True,
            'errors': {}
        })

    except ValidationError as e:
        # Return validation errors
        error_html = render_to_string('partials/form_errors.html', {'errors': e.message_dict})
        yield SSE.patch_elements(error_html, selector='#form-errors')
        yield SSE.patch_signals({'loading': False, 'errors': e.message_dict})

    except Exception as e:
        # Return general error
        errors = {'general': str(e)}
        error_html = render_to_string('partials/form_errors.html', {'errors': errors})
        yield SSE.patch_elements(error_html, selector='#form-errors')
        yield SSE.patch_signals({'loading': False, 'errors': errors})
```

**With Django Forms:**

```python
from django import forms

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['client', 'tour', 'date', 'participants']

@datastar_response
def booking_create(request: HttpRequest):
    """
    Handle form submission using Django Forms.
    """
    form = BookingForm(request.POST)

    if form.is_valid():
        # Add business isolation
        booking = form.save(commit=False)
        booking.business = request.user.business
        booking.save()

        # Success
        success_html = render_to_string('partials/booking_success.html', {'booking': booking})
        yield SSE.patch_elements(success_html, selector='#booking-form-container')
        yield SSE.patch_signals({'loading': False, 'showSuccess': True, 'errors': {}})
    else:
        # Return validation errors
        error_html = render_to_string('partials/form_errors.html', {'errors': form.errors})
        yield SSE.patch_elements(error_html, selector='#form-errors')
        yield SSE.patch_signals({'loading': False, 'errors': form.errors})
```

---
