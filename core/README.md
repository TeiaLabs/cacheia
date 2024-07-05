# Cacheia

Cacheia has all the core functionality for the "cacheia" package. It exposes a simple interface for multiple cache providers with added features like cache invalidation and cache expiration.

## Code

Cacheia mainly exposes one interface to interact with all backends and some custom exceptions:

- Cacheia: The main interface to interact with all backends.
- InvalidSettings: Exception raised when an invalid settings class type is passed to `Cacheia.setup` method.
- KeyAlreadyExists: Exception raised when a key already exists in the cache and the user tries to set it again.
- decorator: Module that exposes a decorator to cache function calls.

## Examples

To create a new cache:

```python
from cacheia import Cacheia
from cacheia_schemas import CachedValue


Cacheia.setup()
cache = Cacheia.get()
instance = CachedValue(key="key", value="value")
cache.cache(instance=instance)
```

---

To get all cached values:

```python
from cacheia import Cacheia


Cacheia.setup()
cache = Cacheia.get()
for value in cache.get():
    print(value)
```

---

To get a value from the cache:

```python
from cacheia import Cacheia


Cacheia.setup()
cache = Cacheia.get()
cached_value = cache.get_key("key")
print(cached_value)
```

---

To flush all values:

```python
from cacheia import Cacheia


Cacheia.setup()
cache = Cacheia.get()
result = cache.flush()
print(result.deleted_count)
```

---

To flush some values:

```python
from datetime import datetime
from cacheia import Cacheia


Cacheia.setup()
cache = Cacheia.get()

now = datetime.now().timestamp()
result = cache.flush(expires_range=(now - 100, now + 100))
print(result.deleted_count)
```

---

To flush a single key:

```python
from cacheia import Cacheia


Cacheia.setup()
cache = Cacheia.get()

result = cache.flush_key(key="key")
print(result.deleted_count)
```
