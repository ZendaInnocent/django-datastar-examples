# Datastar Attributes Reference

## Core Attributes

### `data-signals`

Define initial signals:

```html
<!-- Single signal -->
<div data-signals:count="0"></div>

<!-- Multiple signals -->
<div data-signals="{count: 0, name: 'John', active: true}"></div>

<!-- Nested signals -->
<div data-signals:settings.theme="dark"></div>

<!-- Conditional defaults -->
<div data-signals:theme__ifmissing="light"></div>
```

**Modifiers:**

- `__case` – Converts the casing of the signal name.
  - `.camel` – Camel case: `mySignal` (default)
  - `.kebab` – Kebab case: `my-signal`
  - `.snake` – Snake case: `my_signal`
  - `.pascal` – Pascal case: `MySignal`
- `__ifmissing` – Only patches signals if their keys do not already exist. This is useful for setting defaults without overwriting existing values.

```html
<div
  data-signals:my-signal__case.kebab="1"
  data-signals:foo__ifmissing="1"></div>
```

**Important:** Signals beginning with an underscore are not included in requests to the backend by default. Signal names cannot begin with nor contain a double underscore (`__`), due to its use as a modifier delimiter.

### `data-bind`

Two-way data binding:

```html
<!-- Input binding -->
<input
  type="text"
  data-bind:username />

<!-- Select binding -->
<select data-bind:country>
  <option value="us">USA</option>
  <option value="uk">UK</option>
</select>

<!-- Checkbox group (array) -->
<div data-signals:preferences="[]">
  <input
    type="checkbox"
    data-bind:preferences
    value="newsletter" />
  <input
    type="checkbox"
    data-bind:preferences
    value="sms" />
</div>

<!-- File upload (base64) -->
<input
  type="file"
  data-bind:profileImage
  multiple />
```

**Modifiers:**

- `__case` – Converts the casing of the signal name.
  - `.camel` – Camel case: `mySignal` (default)
  - `.kebab` – Kebab case: `my-signal`
  - `.snake` – Snake case: `my_signal`
  - `.pascal` – Pascal case: `MySignal`

```html
<!-- Kebab case signal name -->
<input data-bind:my-signal__case.kebab />
```

### `data-text`

Bind text content:

```html
<div data-text="$message"></div>
<span data-text="$user.name"></span>
<p data-text="'Hello, ' + $name"></p>
```

### `data-attr`

Set HTML attributes:

```html
<!-- Single attribute -->
<button data-attr:disabled="$loading">Submit</button>

<!-- Multiple attributes -->
<div data-attr="{'aria-label': $label, disabled: $disabled}"></div>
```

### `data-class`

Conditional classes:

```html
<!-- Single class -->
<div data-class:active="$isActive"></div>

<!-- Multiple classes -->
<div
  data-class="{active: $isActive, 'text-red': $error, hidden: $loading}"></div>
```

**Modifiers:**

- `__case` – Converts the casing of the class.
  - `.camel` – Camel case: `myClass`
  - `.kebab` – Kebab case: `my-class` (default)
  - `.snake` – Snake case: `my_class`
  - `.pascal` – Pascal case: `MyClass`

```html
<!-- Camel case class name -->
<div data-class:my-class__case.camel="$foo"></div>
```

### `data-style`

Dynamic inline styles:

```html
<!-- Single style -->
<div data-style:display="$hidden && 'none'"></div>

<!-- Multiple styles -->
<div
  data-style="{
    display: $hidden ? 'none' : 'block',
    color: $urgent ? 'red' : 'blue'
}"></div>
```

### `data-show`

Show/hide elements:

```html
<div data-show="$isLoggedIn">Welcome back!</div>
<div
  data-show="!$isAdmin"
  style="display: none">
  Restricted
</div>
```

## Event Handling Attributes

### `data-on`

Event listeners:

```html
<!-- Click event -->
<button data-on:click="$count++">Increment</button>

<!-- Event with modifiers -->
<button data-on:click__debounce.500ms="submitForm()">Submit</button>

<!-- Prevent default -->
<form data-on:submit__prevent="submitForm(event)"></form>

<!-- Stop propagation -->
<div data-on:click="outer()">
  <button data-on:click__stop="inner()">Click</button>
</div>
```

**Modifiers:**

- `__once` - Trigger only once
- `__passive` - Passive event listener
- `__capture` - Use capture phase
- `__case` - Converts the casing of the event
  - `.camel` - Camel case: `myEvent`
  - `.kebab` - Kebab case: `my-event` (default)
  - `.snake` - Snake case: `my_event`
  - `.pascal` - Pascal case: `MyEvent`
- `__delay.500ms` - Delay execution
- `__debounce.500ms` - Debounce with 500ms
- `__debounce.500ms.leading` - Leading edge debounce
- `__debounce.500ms.notrailing` - No trailing edge
- `__throttle.500ms` - Throttle with 500ms
- `__throttle.500ms.noleading` - No leading edge
- `__throttle.500ms.trailing` - Trailing edge
- `__viewtransition` - Wraps expression in `document.startViewTransition()`
- `__window` - Attach to window
- `__outside` - Trigger on outside click
- `__prevent` - Prevent default behavior
- `__stop` - Stop propagation

### `data-on-interval`

Periodic execution:

```html
<!-- Every second (default) -->
<div data-on-interval="$count++"></div>

<!-- Custom interval -->
<div data-on-interval__duration.5s="refreshData()"></div>

<!-- Immediate execution -->
<div data-on-interval__duration.1s.leading="$count++"></div>
```

**Modifiers:**

- `__duration` – Sets the interval duration.
  - `.500ms` – Interval duration of 500 milliseconds (accepts any integer).
  - `.1s` – Interval duration of 1 second (default).
  - `.leading` – Execute the first interval immediately.
- `__viewtransition` – Wraps the expression in `document.startViewTransition()` when the View Transition API is available.

### `data-on-intersect`

Viewport intersection:

```html
<!-- When visible -->
<div data-on-intersect="$visible = true"></div>

<!-- Half visible -->
<div data-on-intersect__half="loadContent()"></div>

<!-- Fully visible -->
<div data-on-intersect__full="playVideo()"></div>

<!-- Custom threshold -->
<div data-on-intersect__threshold.75="triggerAction()"></div>

<!-- Only once -->
<div data-on-intersect__once="lazyLoadImage()"></div>

<!-- On exit -->
<div data-on-intersect__exit="pauseVideo()"></div>
```

**Modifiers:**

- `__once` – Only triggers the event once.
- `__exit` – Only triggers the event when the element exits the viewport.
- `__half` – Triggers when half of the element is visible.
- `__full` – Triggers when the full element is visible.
- `__threshold` – Triggers when the element is visible by a certain percentage.
  - `.25` – Triggers when 25% of the element is visible.
  - `.75` – Triggers when 75% of the element is visible.
- `__delay` – Delay the event listener.
  - `.500ms` – Delay for 500 milliseconds (accepts any integer).
  - `.1s` – Delay for 1 second (accepts any integer).
- `__debounce` – Debounce the event listener.
  - `.500ms` – Debounce for 500 milliseconds (accepts any integer).
  - `.1s` – Debounce for 1 second (accepts any integer).
  - `.leading` – Debounce with leading edge (must come after timing).
  - `.notrailing` – Debounce without trailing edge (must come after timing).
- `__throttle` – Throttle the event listener.
  - `.500ms` – Throttle for 500 milliseconds (accepts any integer).
  - `.1s` – Throttle for 1 second (accepts any integer).
  - `.noleading` – Throttle without leading edge (must come after timing).
  - `.trailing` – Throttle with trailing edge (must come after timing).
- `__viewtransition` – Wraps the expression in `document.startViewTransition()` when the View Transition API is available.

## Advanced Attributes

### `data-indicator`

Loading indicators:

```html
<button
  data-on:click="@get('/api/data')"
  data-indicator:loading
  data-attr:disabled="$loading">
  Load Data
</button>

<div data-show="$loading">Loading...</div>
```

**Modifiers:**

- `__case` – Converts the casing of the signal name.
  - `.camel` – Camel case: `mySignal` (default)
  - `.kebab` – Kebab case: `my-signal`
  - `.snake` – Snake case: `my_signal`
  - `.pascal` – Pascal case: `MySignal`

```html
<!-- Kebab case signal name -->
<button data-indicator:my-signal__case.kebab></button>
```

### `data-effect`

Side effects on signal change:

```html
<!-- Update another signal -->
<div data-effect="$total = $price * $quantity"></div>

<!-- Call function on change -->
<div data-effect="validateForm()"></div>

<!-- Multiple effects -->
<div data-effect="updateTotal(); validate();"></div>
```

### `data-computed`

Computed signals (read-only):

```html
<!-- Single computed -->
<div data-computed:total="$price * $quantity"></div>

<!-- Multiple computed -->
<div
  data-computed="{
    total: () => $price * $quantity,
    tax: () => $total * 0.1,
    grandTotal: () => $total + $tax
  }"></div>
```

**Modifiers:**

- `__case` – Converts the casing of the signal name.
  - `.camel` – Camel case: `mySignal` (default)
  - `.kebab` – Kebab case: `my-signal`
  - `.snake` – Snake case: `my_signal`
  - `.pascal` – Pascal case: `MySignal`

```html
<div data-computed:my-signal__case.kebab="$bar + $baz"></div>
```

**Important:** Computed signal expressions must not be used for performing actions (changing other signals, actions, JavaScript functions, etc.). If you need to perform an action in response to a signal change, use the `data-effect` attribute.

### `data-on-signal-patch`

React to signal changes:

```html
<!-- On any signal change -->
<div data-on-signal-patch="console.log('Changed:', patch)"></div>

<!-- The patch variable is available in expression -->
<div data-on-signal-patch="console.log('Signal patch:', patch)"></div>
```

**Modifiers:**

- `__delay` – Delay the event listener.
  - `.500ms` – Delay for 500 milliseconds (accepts any integer).
  - `.1s` – Delay for 1 second (accepts any integer).
- `__debounce` – Debounce the event listener.
  - `.500ms` – Debounce for 500 milliseconds (accepts any integer).
  - `.1s` – Debounce for 1 second (accepts any integer).
  - `.leading` – Debounce with leading edge (must come after timing).
  - `.notrailing` – Debounce without trailing edge (must come after timing).
- `__throttle` – Throttle the event listener.
  - `.500ms` – Throttle for 500 milliseconds (accepts any integer).
  - `.1s` – Throttle for 1 second (accepts any integer).
  - `.noleading` – Throttle without leading edge (must come after timing).
  - `.trailing` – Throttle with trailing edge (must come after timing).

### `data-on-signal-patch-filter`

Filters which signals to watch when using `data-on-signal-patch`.

The `data-on-signal-patch-filter` attribute accepts an object with `include` and/or `exclude` properties that are regular expressions.

```html
<!-- Only react to counter signal changes -->
<div data-on-signal-patch-filter="{include: /^counter$/}"></div>

<!-- React to all changes except those ending with "changes" -->
<div data-on-signal-patch-filter="{exclude: /changes$/}"></div>

<!-- Combine include and exclude filters -->
<div data-on-signal-patch-filter="{include: /user/, exclude: /password/}"></div>
```

### `data-on-signal-patch-filter`

Filters which signals to watch when using `data-on-signal-patch`.

```html
<!-- Only react to counter signal changes -->
<div data-on-signal-patch-filter="{include: /^counter$/}"></div>

<!-- React to all changes except those ending with "changes" -->
<div data-on-signal-patch-filter="{exclude: /changes$/}"></div>

<!-- Combine include and exclude filters -->
<div data-on-signal-patch-filter="{include: /user/, exclude: /password/}"></div>
```

### `data-ref`

Element references:

```html
<!-- Create reference -->
<input data-ref:usernameInput />

<!-- Use reference -->
<button data-on:click="$usernameInput.focus()">Focus</button>
```

**Modifiers:**

- `__case` – Converts the casing of the signal name.
  - `.camel` – Camel case: `mySignal` (default)
  - `.kebab` – Kebab case: `my-signal`
  - `.snake` – Snake case: `my_signal`
  - `.pascal` – Pascal case: `MySignal`

```html
<div data-ref:my-signal__case.kebab></div>
```

### `data-init`

Initialize on load:

```html
<!-- Simple initialization -->
<div data-init="$count = 0"></div>

<!-- With delay -->
<div data-init__delay.100ms="initialize()"></div>
```

**Modifiers:**

- `__delay` – Delay the event listener.
  - `.500ms` – Delay for 500 milliseconds (accepts any integer).
  - `.1s` – Delay for 1 second (accepts any integer).
- `__viewtransition` – Wraps the expression in `document.startViewTransition()` when the View Transition API is available.

## Utility Attributes

### `data-json-signals`

Debug signals:

```html
<!-- Show all signals -->
<pre data-json-signals></pre>

<!-- Filtered display -->
<pre data-json-signals="{include: /user/}"></pre>
<pre data-json-signals="{exclude: /password/}"></pre>

<!-- Compact format -->
<pre data-json-signals__terse="{include: /count/}"></pre>
```

### `data-ignore`

Ignore processing:

```html
<!-- Ignore element and children -->
<div data-ignore>
  <div>Not processed by Datastar</div>
</div>

<!-- Ignore only element -->
<div data-ignore__self>
  <div>This is processed</div>
</div>
```

### `data-ignore-morph`

Ignore during morphing:

```html
<div data-ignore-morph>This element won't be morphed</div>
```

### `data-preserve-attr`

Preserve attributes:

```html
<!-- Preserve single attribute -->
<details
  open
  data-preserve-attr="open">
  <summary>Title</summary>
  Content
</details>

<!-- Preserve multiple attributes -->
<details
  open
  class="expanded"
  data-preserve-attr="open class"></details>
```

---
