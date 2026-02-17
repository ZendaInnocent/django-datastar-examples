# Version Compatibility

## Frontend

- **Datastar**: v1.0.0-RC.7 (recommended for production)
- **Browser Support**: Modern browsers supporting ES2020+ and EventSource API

## Backend (Python)

- **datastar-py**: v0.8.0+ (latest)
- **Python**: 3.8+
- **Django**: 3.2+

## Version Pinning Strategy

Always use specific version:

```html
<script src="https://cdn.jsdelivr.net/gh/starfederation/datastar@v1.0.0-RC.7/bundles/datastar.js"></script>
```

## Breaking Changes

### v1.0.0-RC.7

- No breaking changes from RC6
- Added `data-on-signal-patch-filter` attribute
- Improved modifier syntax consistency

### v1.0.0-RC series

- All core features are stable
- API considered frozen for 1.0.0 release
- Minor documentation and performance improvements expected

---

_Always test upgrades in development before deploying to production._
