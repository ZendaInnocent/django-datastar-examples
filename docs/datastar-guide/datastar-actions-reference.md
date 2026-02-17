# Datastar Actions Reference

Datastar provides actions (helper functions) that can be used in Datastar expressions. The `@` prefix designates actions that are safe to use in expressions and executed in a secure sandboxed environment.

## Core Actions

### `@peek()`

Access signals without subscribing to their changes.

```html
<!-- Re-evaluates when $foo changes, NOT when $bar changes -->
<div data-text="$foo + @peek(() => $bar)"></div>
```

Use case: Display a signal value in an expression without triggering re-evaluation when that signal changes.

### `@setAll()`

Set value of all matching signals.

```html
<!-- Set single signal -->
<div data-signals:foo="false">
  <button data-on:click="@setAll(true, {include: /^foo$/})">Set True</button>
</div>

<!-- Set all signals starting with 'user.' -->
<div data-signals="{user: {name: '', nickname: ''}}">
  <button data-on:click="@setAll('johnny', {include: /^user\./})">
    Set All User
  </button>
</div>

<!-- Set all except those ending with '_temp' -->
<div data-signals="{data: '', data_temp: '', info: '', info_temp: ''}">
  <button data-on:click="@setAll('reset', {include: /.*/, exclude: /_temp$/})">
    Reset
  </button>
</div>
```

**Parameters:**

- `value` - Value to set
- `filter` (optional) - Filter object with `include` and `exclude` regex patterns

### `@toggleAll()`

Toggle boolean value of all matching signals.

```html
<!-- Toggle single signal -->
<div data-signals:foo="false">
  <button data-on:click="@toggleAll({include: /^foo$/})">Toggle</button>
</div>

<!-- Toggle all signals starting with 'is' -->
<div data-signals="{isOpen: false, isActive: true, isEnabled: false}">
  <button data-on:click="@toggleAll({include: /^is/})">Toggle All</button>
</div>

<!-- Toggle nested signals -->
<div data-signals="{settings: {darkMode: false, autoSave: true}}">
  <button data-on:click="@toggleAll({include: /^settings\./})">
    Toggle Settings
  </button>
</div>
```

**Parameters:**

- `filter` (optional) - Filter object with `include` and `exclude` regex patterns

### `@fit()`

Linearly interpolate a value from one range to another.

```html
<!-- Convert 0-100 slider to 0-255 RGB value -->
<input
  type="range"
  min="0"
  max="100"
  value="50"
  data-bind:sliderValue />
<div data-computed:rgbValue="@fit($sliderValue, 0, 100, 0, 255)">
  RGB: <span data-text="$rgbValue"></span>
</div>

<!-- Convert Celsius to Fahrenheit -->
<input
  type="number"
  data-bind:celsius
  value="20" />
<div data-computed:fahrenheit="@fit($celsius, 0, 100, 32, 212)">
  <span data-text="$celsius"></span>°C =
  <span data-text="$fahrenheit.toFixed(1)"></span>°F
</div>

<!-- Map mouse position to opacity (clamped) -->
<div
  data-signals:mouseX="0"
  data-computed:opacity="@fit($mouseX, 0, window.innerWidth, 0, 1, true)"
  data-on:mousemove__window="$mouseX = evt.clientX"
  data-attr:style="'opacity: ' + $opacity">
  Move mouse horizontally
</div>
```

**Parameters:**

- `v` - Value to convert
- `oldMin` - Old range minimum
- `oldMax` - Old range maximum
- `newMin` - New range minimum
- `newMax` - New range maximum
- `shouldClamp` (optional) - Clamp result to new range
- `shouldRound` (optional) - Round result to nearest integer

## Backend Actions

Backend actions send HTTP requests to your Django views.

### `@get()`

Send GET request to backend.

```html
<!-- Basic GET request -->
<button data-on:click="@get('/tours')">Load Tours</button>

<!-- With options -->
<button
  data-on:click="@get('/tours', {
    filterSignals: {include: /tour/},
    openWhenHidden: true
})">
  Load Tours
</button>
```

### `@post()`

Send POST request to backend.

```html
<!-- Basic POST request -->
<button data-on:click="@post('/bookings/create')">Create Booking</button>

<!-- POST with form data -->
<form id="booking-form">
  <input data-bind:clientName />
  <button data-on:click="@post('/bookings/create', {contentType: 'form'})">
    Submit
  </button>
</form>
```

### `@put()`

Send PUT request to backend.

```html
<button data-on:click="@put('/tours/1')">Update Tour</button>
```

### `@patch()`

Send PATCH request to backend.

```html
<button
  data-on:click="@patch('/tours/1', {
    payload: {title: 'Updated Tour'}
})">
  Patch Tour
</button>
```

### `@delete()`

Send DELETE request to backend.

```html
<button data-on:click="@delete('/tours/1')">Delete Tour</button>
```

## Action Options

All backend actions (`@get`, `@post`, `@put`, `@patch`, `@delete`) accept options:

| Option                | Type                                             | Default                            | Description                                     |
| --------------------- | ------------------------------------------------ | ---------------------------------- | ----------------------------------------------- |
| `contentType`         | `'json'` \| `'form'`                             | `'json'`                           | How to send data (JSON signals or form data)    |
| `filterSignals`       | `{include: RegExp, exclude?: RegExp}`            | `{include: /.*/}`                  | Filter which signals to send                    |
| `selector`            | `string` \| `null`                               | `null`                             | CSS selector for form (when contentType='form') |
| `headers`             | `object`                                         | `{}`                               | Custom HTTP headers                             |
| `openWhenHidden`      | `boolean`                                        | `false` for GET, `true` for others | Keep connection open when page hidden           |
| `payload`             | `object`                                         | `null`                             | Override fetch payload with custom object       |
| `retry`               | `'auto'` \| `'error'` \| `'always'` \| `'never'` | `'auto'`                           | When to retry requests                          |
| `retryInterval`       | `number`                                         | `1000`                             | Retry interval in milliseconds                  |
| `retryScaler`         | `number`                                         | `2`                                | Numeric multiplier for retry wait times         |
| `retryMaxWaitMs`      | `number`                                         | `30000`                            | Maximum wait time between retries               |
| `retryMaxCount`       | `number`                                         | `10`                               | Maximum number of retry attempts                |
| `requestCancellation` | `'auto'` \| `'disabled'` \| `AbortController`    | `'auto'`                           | Request cancellation behavior                   |

### contentType Option

```html
<!-- JSON (default) - sends all signals -->
<button data-on:click="@post('/endpoint', {contentType: 'json'})">
  Submit JSON
</button>

<!-- Form - uses closest form elements -->
<form id="my-form">
  <input
    name="username"
    data-bind:username />
  <button data-on:click="@post('/endpoint', {contentType: 'form'})">
    Submit Form
  </button>
</form>

<!-- Form with specific selector -->
<button
  data-on:click="@post('/endpoint', {
    contentType: 'form',
    selector: '#my-form'
})">
  Submit Specific Form
</button>
```

### filterSignals Option

```html
<!-- Include only matching signals -->
<button
  data-on:click="@get('/endpoint', {
    filterSignals: {include: /^tour\./}
})">
  Load Tour Data
</button>

<!-- Include but exclude patterns -->
<button
  data-on:click="@get('/endpoint', {
    filterSignals: {include: /^user/, exclude: /password/}
})">
  Load User Profile
</button>
```

### headers Option

```html
<button
  data-on:click="@get('/endpoint', {
    headers: {
        'X-Custom-Header': 'value',
        'Authorization': 'Bearer token'
    }
})">
  With Headers
</button>
```

### openWhenHidden Option

```html
<!-- Keep connection open when tab is hidden -->
<div
  data-on-interval__duration.60s
  data-init="@get('/dashboard', {openWhenHidden: true})"></div>
```

Useful for dashboards that should update even when in background tab.

### payload Option

```html
<!-- Override signals with custom payload -->
<button
  data-on:click="@post('/endpoint', {
    payload: {
        customField: 'value',
        anotherField: 123
    }
})">
  With Custom Payload
</button>
```

### retry Option

```html
<!-- Retry on errors -->
<button
  data-on:click="@get('/endpoint', {
    retry: 'error'
})">
  Retry on Error
</button>

<!-- Always retry -->
<button
  data-on:click="@get('/endpoint', {
    retry: 'always',
    retryMaxCount: 3
})">
  Always Retry
</button>

<!-- Never retry -->
<button
  data-on:click="@get('/endpoint', {
    retry: 'never'
})">
  No Retry
</button>
```

**Retry Options:**

- `'auto'` - Retries on network errors only (default)
- `'error'` - Retries on 4xx and 5xx responses
- `'always'` - Retries on all non-204 responses (except redirects)
- `'never'` - Disables retries

### requestCancellation Option

```html
<!-- Auto cancel (default) - cancels previous requests -->
<button data-on:click="@get('/endpoint')">
  Click Multiple Times - Only Last Request Runs
</button>

<!-- Disabled - allows concurrent requests -->
<button
  data-on:click="@get('/endpoint', {
    requestCancellation: 'disabled'
})">
  Allow Concurrent Requests
</button>

<!-- Custom AbortController -->
<div data-signals:controller="new AbortController()">
  <button
    data-on:click="@get('/endpoint', {
        requestCancellation: $controller
    })">
    Start Request
  </button>
  <button data-on:click="$controller.abort()">Cancel Request</button>
</div>
```

## Request Cancellation

By default, Datastar automatically cancels previous requests on the same element when a new request is initiated:

```html
<!-- Clicking multiple times cancels previous requests -->
<button data-on:click="@get('/slow-endpoint')">Load Data</button>
```

This prevents multiple concurrent requests and ensures clean state management. Requests on different elements can run concurrently.

## Response Handling

Backend actions automatically handle different response content types:

### text/event-stream (SSE)

Standard SSE responses with Datastar events (default for Django views decorated with `@datastar_response`).

```python
@datastar_response
def my_view(request):
    yield SSE.patch_elements("<div>Hello</div>")
    yield SSE.patch_signals({'count': 1})
```

### text/html

HTML elements to patch into DOM.

```python
from django.http import HttpResponse

def my_view(request):
    response = HttpResponse('<p>New content</p>', content_type='text/html')
    response['datastar-selector'] = '#my-element'
    response['datastar-mode'] = 'inner'
    return response
```

**Response Headers:**

- `datastar-selector` - CSS selector for target elements
- `datastar-mode` - How to patch (outer, inner, replace, prepend, append, before, after)
- `datastar-use-view-transition` - Use View Transition API

### application/json

JSON encoded signals to patch.

```python
import json
from django.http import HttpResponse

def my_view(request):
    response = HttpResponse(
        json.dumps({'foo': 'bar'}),
        content_type='application/json'
    )
    response['datastar-only-if-missing'] = 'true'
    return response
```

**Response Headers:**

- `datastar-only-if-missing` - Only patch signals that don't exist

### text/javascript

JavaScript code to execute in browser.

```python
import json
from django.http import HttpResponse

def my_view(request):
    response = HttpResponse(
        'console.log("Hello from server!");',
        content_type='text/javascript'
    )
    response['datastar-script-attributes'] = json.dumps({'type': 'module'})
    return response
```

**Response Headers:**

- `datastar-script-attributes` - Script element attributes (JSON encoded)

## Fetch Events

Backend actions trigger `datastar-fetch` events during request lifecycle:

```html
<div data-on:datastar-fetch="console.log('Fetch:', evt.detail.type)"></div>
```

**Event Types:**

- `started` - Fetch request started
- `finished` - Fetch request finished
- `error` - Fetch request encountered error
- `retrying` - Fetch request is retrying
- `retries-failed` - All retries failed

```html
<!-- Show loading on fetch start -->
<div
  data-on:datastar-fetch="$loading = evt.detail.type === 'started' || evt.detail.type === 'retrying'"
  data-show="$loading">
  Loading...
</div>
```

```html
<!-- Handle fetch errors -->
<div
  data-on:datastar-fetch="
    evt.detail.type === 'error' && showError('Request failed');
    evt.detail.type === 'retries-failed' && showError('All retries failed')
"></div>
```

---
