# Python SDK API

## Supported Frameworks

`datastar-py` supports multiple web frameworks with framework-specific helpers, for this project we only django:

- **Django** - `from datastar_py.django import datastar_response, read_signals, ServerSentEventGenerator as SSE`

## Django Module

```python
from datastar_py.django import (
    datastar_response,    # Decorator for views
    read_signals,         # Read client signals
    ServerSentEventGenerator as SSE,                  # Server-Sent Event generator
    DatastarResponse,     # Response class
    SSE_HEADERS,          # SSE headers
)
```

## `datastar_response`

Decorator that wraps view return in `DatastarResponse`:

```python
# Sync view
@datastar_response
def my_view(request):
    yield SSE.patch_signals({'count': 1})

# Async view
@datastar_response
async def async_view(request):
    await asyncio.sleep(1)
    yield SSE.patch_signals({'count': 2})

# Generator view (long-lived stream)
@datastar_response
async def stream_view(request):
    for i in range(10):
        yield SSE.patch_signals({'count': i})
        await asyncio.sleep(1)
```

## `read_signals`

Read signals from request:

```python
signals = read_signals(request)

# Access signals
count = signals.get('count')
name = signals.get('name')
settings = signals.get('settings')

# Check if signal exists
if 'userId' in signals:
    user_id = signals['userId']
```

## SSE (Server-Sent Event Generator)

### `SSE.patch_elements`

Patch HTML elements:

```python
# Basic usage
yield SSE.patch_elements("<div>Hello</div>", selector="#target")

# With mode
yield SSE.patch_elements(
    "<div>New content</div>",
    selector="#target",
    mode="outer"  # outer, inner, replace, append, prepend, before, after
)

# With view transition
yield SSE.patch_elements(
    "<div>Content</div>",
    selector="#target",
    use_view_transition=True
)

# SVG namespace
yield SSE.patch_elements(
    "<svg><circle/></svg>",
    selector="#svg-target",
    namespace="svg"
)
```

**Modes:**

- `outer` - Morph element (default)
- `inner` - Replace inner HTML
- `replace` - Replace entire element
- `append` - Append inside element
- `prepend` - Prepend inside element
- `before` - Insert before element
- `after` - Insert after element

### `SSE.remove_elements`

Remove elements:

```python
yield SSE.remove_elements(selector="#remove-me")
```

### `SSE.patch_signals`

Update client signals:

```python
# Simple signal
yield SSE.patch_signals({'count': 10})

# Nested signals
yield SSE.patch_signals({'user': {'name': 'John', 'age': 30}})

# Only if missing
yield SSE.patch_signals({'theme': 'light'}, only_if_missing=True)

# Remove signal
yield SSE.patch_signals({'temp': None})
```

### `SSE.execute_script`

Execute JavaScript:

```python
# Simple script
yield SSE.execute_script("alert('Hello!')")

# With custom attributes
yield SSE.execute_script(
    "console.log('test')",
    attributes={'id': 'script-1'},
    auto_remove=False
)
```

### `SSE.redirect`

Redirect browser:

```python
yield SSE.redirect('/dashboard')
```

## DatastarResponse

Direct response creation:

```python
# Empty response (204)
response = DatastarResponse()

# Single event
response = DatastarResponse(
    SSE.patch_elements("<div>Hello</div>")
)

# Multiple events
response = DatastarResponse([
    SSE.patch_elements("<div>Hello</div>"),
    SSE.patch_signals({'count': 1})
])

# With custom headers
response = DatastarResponse(
    SSE.patch_signals({'data': 'value'}),
    status=200,
    headers={'X-Custom-Header': 'value'}
)
```

## Attribute Generation Helper

Datastar allows HTML generation to be done on the backend. `datastar-py` includes a helper to generate data-\* attributes in your HTML with IDE completion and type checking.

```python
from datastar_py import attribute_generator as data
```

### Usage with HTML Libraries

```python
# htpy
button(data.on("click", "console.log('clicked')").debounce(1000).stop)["My Button"]

# FastHTML
Button("My Button", data.on("click", "console.log('clicked')").debounce(1000).stop)
Button(data.on("click", "console.log('clicked')").debounce(1000).stop)("My Button")

# f-strings
f"<button {data.on('click', 'console.log(\'clicked\')').debounce(1000).stop}>My Button</button>"

# Jinja (no editor completion)
<button {{data.on("click", "console.log('clicked')").debounce(1000).stop}}>My Button</button>
```

### Custom Alias Support

When using datastar with a different alias, you can instantiate the class yourself:

```python
from datastar_py.attributes import AttributeGenerator

data = AttributeGenerator(alias="data-star-")

# htmy (htmy will transform _ into - unless attribute starts with _, which will be stripped)
data = AttributeGenerator(alias="_data-")
html.button("My Button", **data.on("click", "console.log('clicked')").debounce("1s").stop)
```

---
