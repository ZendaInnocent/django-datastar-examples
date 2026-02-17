# Error Handling

Datastar has built-in error handling and reporting for runtime errors. When a data attribute is used incorrectly, detailed error messages are logged to the browser console.

## Console Error Messages

When a data attribute is used incorrectly, Datastar logs structured error messages:

```javascript
Uncaught datastar runtime error: errorType
More info: https://data-star.dev/errors/errorType?metadata={encodedContext}
Context: {
    "plugin": {
        "name": "pluginName",
        "type": "attribute"
    },
    "element": {
        "id": "elementId",
        "tag": "DIV"
    },
    "expression": {
        "rawKey": "originalKey",
        "key": "processedKey",
        "value": "expressionValue",
        "fnContent": "functionContent"
    }
}
```

## Common Error Types

### `keyNotAllowed`

Occurs when using invalid keys in data attributes:

```html
<!-- This will cause an error -->
<div data-text-foo="$message"></div>
```

**Fix:** Use correct attribute syntax:

```html
<!-- Correct syntax -->
<div data-text="$message"></div>
```

### `signalNotFound`

Occurs when referencing undefined signals:

```html
<!-- This will cause an error if $user is not defined -->
<div data-text="$user.name"></div>
```

**Fix:** Define the signal first:

```html
<div data-signals:user="{}">
  <div data-text="$user.name"></div>
</div>
```

### `expressionEvaluationFailed`

Occurs when JavaScript expressions have syntax errors or runtime failures:

```html
<!-- This will cause an error -->
<div data-text="$undefinedVariable + 1"></div>
```

**Fix:** Ensure all variables are defined and expressions are valid:

```html
<div data-text="$count + 1"></div>
```

## Debugging Tips

### Use `data-json-signals` for Debugging

Display all current signals to troubleshoot issues:

```html
<!-- Show all signals -->
<pre data-json-signals></pre>

<!-- Show specific signals -->
<pre data-json-signals="{include: /^user/}"></pre>

<!-- Compact format for inline debugging -->
<span data-json-signals__terse="{include: /count/}"></span>
```

### Browser Developer Tools

1. **Console:** Check for Datastar error messages
2. **Network Tab:** Monitor SSE events in real-time
3. **Elements Tab:** Inspect data attributes on elements

### Datastar Inspector (Pro)

Datastar Pro includes an Inspector tool for monitoring and debugging SSE events.

## Preventing Common Errors

### 1. Always Define Signals Before Using

```html
<!-- Good: Define first -->
<div data-signals:count="0">
  <div data-text="$count"></div>
</div>

<!-- Bad: Using undefined signal -->
<div data-text="$count"></div>
```

### 2. Use Correct Attribute Syntax

```html
<!-- Good: Proper syntax -->
<div data-text="$message"></div>
<div data-class:active="$isActive"></div>

<!-- Bad: Invalid syntax -->
<div
  data-text="$message"
  data-class-active="$isActive"></div>
```

### 3. Validate Expressions

```html
<!-- Good: Valid expression -->
<div data-computed:total="$price * $quantity"></div>

<!-- Bad: Undefined function -->
<div data-computed:total="multiply($price, $quantity)"></div>
```

### 4. Handle Missing Values

```html
<!-- Good: Handle missing nested properties -->
<div data-text="$user?.name || 'Guest'"></div>

<!-- Bad: Accessing undefined nested property -->
<div data-text="$user.name"></div>
```

## Error Context Information

Each error includes contextual metadata:

- **Plugin:** Which Datastar plugin encountered the error
- **Element:** DOM element information (tag, ID, classes)
- **Expression:** Details about the parsed expression

Use this information to quickly locate and fix problematic code.

---

_For a complete list of error types and solutions, visit [Datastar Errors](https://data-star.dev/errors)_
