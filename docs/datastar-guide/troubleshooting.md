# Troubleshooting

## Issue: Signals Not Updating

**Problem:** Signals sent from server aren't updating on client.

**Solution:**

```python
# Ensure you're using yield, not return
@datastar_response
def my_view(request):
    # ✅ Correct
    yield SSE.patch_signals({'count': 1})

    # ❌ Wrong
    return SSE.patch_signals({'count': 1})
```

## Issue: CSS Styles Lost After Update

**Problem:** After DOM morphing, element styles are lost.

**Solution:**

```html
<!-- Use data-preserve-attr -->
<div data-preserve-attr="style class">Your content</div>
```

## Issue: Input Focus Lost

**Problem:** Input loses focus when updating related content.

**Solution:**

```python
# Use specific selector, don't update entire form
yield SSE.patch_elements(html, selector='#related-info')
# Not selector='form' or selector='body'
```

## Issue: Too Many Requests

**Problem:** Search/polling causing excessive requests.

**Solution:**

```html
<!-- Use debounce for search -->
<input data-on:input__debounce.300ms="@get('/search')" />

<!-- Use throttle for polling (min 5s) -->
<div data-on-interval__duration.5s="refresh()"></div>
```

## Issue: Memory Leaks in Long-Lived Streams

**Problem:** Memory grows over time with streaming views.

**Solution:**

```python
@datastar_response
async def stream_view(request):
    try:
        while True:
            # Process data
            yield SSE.patch_elements(html, selector='#content')
            await asyncio.sleep(2)

            # Break condition
            if should_stop():
                break
    except GeneratorExit:
        # Clean up resources
        logger.info("Stream closed by client")
    finally:
        # Final cleanup
        cleanup_resources()
```

## Issue: CSRF Token Missing

**Problem:** POST requests failing with CSRF error.

**Solution:**

```python
# Datastar-py handles CSRF automatically for forms
# Ensure your form includes {% csrf_token %}

<form data-on:submit="@post('/submit')">
    {% csrf_token %}
    <input data-bind:username>
    <button>Submit</button>
</form>
```

## Issue: Nested Signals Not Working

**Problem:** Nested signal paths (e.g., `user.name`) not updating.

**Solution:**

```html
<!-- Define nested signals -->
<div data-signals="{user: {name: 'John', email: 'john@example.com'}}">
  <!-- Access nested signals -->
  <div data-text="$user.name"></div>
  <div data-text="$user.email"></div>
</div>

<!-- Update from server -->
yield SSE.patch_signals({ 'user': { 'name': 'Jane', 'email': 'jane@example.com'
} })
```

## Issue: Datastar Not Initializing

**Problem:** Datastar attributes not working at all.

**Solution:**

```html
<!-- Ensure CDN script is included -->
<script
  type="module"
  src="https://cdn.jsdelivr.net/gh/starfederation/datastar@latest/bundles/datastar.js"></script>

<!-- Check browser console for errors -->
<!-- Ensure no JavaScript errors before Datastar loads -->
```

---
