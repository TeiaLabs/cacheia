# Cacheia

Cacheia has all the core functionality for the "cacheia" package. It exposes a simple interface for multiple cache providers with added features like cache invalidation and cache expiration.

## Code

Cacheia mainly exposes one interface to interact with all backends and some custom exceptions:

-   Cacheia: The main interface to interact with all backends.
-   InvalidBackendName: Exception raised when an invalid backend name is passed to any methods of Cacheia.
-   InvalidExpireRange: Exception raised when an invalid expire range is passed as filter to bulk operations such as flush_some and get_all.
-   KeyAlreadyExists: Exception raised when a key already exists in the cache and the user tries to set it again.

## Examples

To create a new cache:

```python
from cacheia import Cacheia
from cacheia_schemas import Backend, Infostar, NewCachedValue


creator = Infostar(org_handle="handle", service_handle="handle")
backend = Backend.MEMORY
instance = NewCachedValue(key="key", value="value")
Cacheia.create_cache(creator=creator, backend=backend, instance=instance)
```

---

To get all cached values:

```python
from cacheia import Cacheia


cached_values = Cacheia.get_all()
for value in cached_values:
    print(value)
```

> Since backend was ommited, Cacheia will search all supported backends to query values.

---

To get a value from the cache:

```python
from cacheia import Cacheia
from cacheia_schemas import Backend


backend = Backend.MEMORY
cached_value = Cacheia.get(backend=backend, key="key")
print(cached_value)
```

---

To flush all values:

```python
from cacheia import Cacheia
from cacheia_schemas import Backend


backend = Backend.MEMORY
expired_only = True # This will only flush expired keys
result = Cacheia.flush_all(backend=backend, expired_only=expired_only)
```

---

To flush some values:

```python
from datetime import datetime
from cacheia import Cacheia
from cacheia_schemas import Backend

now = datetime.now().timestamp()

backend = Backend.MEMORY
expires_range = f"{now - 100}...{now+100}"
result = Cacheia.flush_some(backend=backend, expires_range=expires_range)
print(result.deleted_count)
```

---

To flush a single key:

```python
from cacheia import Cacheia
from cacheia_schemas import Backend


backend = Backend.MEMORY
result = Cacheia.flush_one(backend=backend, key="key")
print(result.deleted_count)
```
