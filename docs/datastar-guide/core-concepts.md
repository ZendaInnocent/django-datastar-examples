# Core Concepts

## Signals

Signals are reactive state variables that live on the client:

```html
<!-- Define initial signals -->
<div data-signals="{count: 0, name: 'World'}">
  <!-- Access signals -->
  <div data-text="$name"></div>
  <!-- Displays: World -->
  <div data-text="$count"></div>
  <!-- Displays: 0 -->
</div>
```

## SSE Events

Server-Sent Events push updates from server to client:

```python
# Django view yields SSE events
yield SSE.patch_elements("<div>Hello</div>", selector="#target")
yield SSE.patch_signals({"count": 5})
```

## Partial Templates

HTML fragments for targeted DOM updates:

```html
<!-- templates/partials/item.html -->
<div
  id="item-{{ item.id }}"
  class="item">
  <h3>{{ item.name }}</h3>
  <p>{{ item.description }}</p>
</div>
```

## DOM Morphing

Intelligent DOM diffing that preserves:

- Input focus
- Scroll position
- Video playback state
- CSS animations

---
