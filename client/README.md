# Cacheia CLient

This module contains a client that is responsible for communicating with the Cacheia API. It is a simple wrapper around the API endpoints, providing a more user-friendly interface for the user.

## Client Methods

-   `cache`: Takes instance (CreateRequest), creator (Infostar) and backend to create a new cache instance in the provided backend.
-   `get`: Retrieves all cached values with optional filters group (str), expires_range (tuple[float, float]) and creation_range(tuple[datetime, datetime]);
-   `get_key`: Fetches the cached value associated with key (str) - Optionally accepts `allow_expired` parameter to return a cached value even if expired.
-   `flush`: Clears all keys from the cache using with optional filters group (str), expires_range (tuple[float, float]) and creation_range(tuple[datetime, datetime]) and return the count of deleted records.
-   `flush_key`: Removes a single key from the cache using key (str).
-   `clear`: Removes all cached values from cache without any validation.

## Code

The library exposes single functions that are similar to `requests` and `httpx` and also exposes a `Client` class that can be used to define default value for API URL.

## Examples

To create a cache instance with the client:

```python
from cacheia_client import Client
from cacheia_schemas import CachedValue


default_url: str = "http://localhost:5000"

client = Client(url=default_url)
instance = CachedValue(key="key", value="value")

client.cache(instance=instance)
```

Or using the helper functions:

```python
from cacheia_client import cache, configure
from cacheia_schemas import CachedValue


configure("http://localhost:5000")

instance = CachedValue(key="key", value="value")
cache(instance=instance)
```

Notice that when calling directly the functions, it is necessary to call "configure"
with the desired URL. Otherwise, it will fail.

---

To get all cached values:

```python
from cacheia_client import Client


default_url: str = "http://localhost:5000"
client = Client(url=default_url)

for v in client.get_all():
    print(v)
```

---

To get a single cached value:

```python
from cacheia_client import Client


default_url: str = "http://localhost:5000"
client = Client(url=default_url)
print(client.get(key="key"))
```

---

To flush all keys:

```python
from cacheia_client import Client


default_url: str = "http://localhost:5000"
client = Client(url=default_url)

result = client.flush()
print(result.deleted_count)
```

---

To flush some keys:

```python
from datetime import datetime
from cacheia_client import Client


default_url: str = "http://localhost:5000"
client = Client(url=default_url)

now = datetime.now().timestamp()
result = client.flush(expires_range=(now-10, now+10))
print(result.deleted_count)
```

---

To flush a single key:

```python
from cacheia_client import Client


default_url: str = "http://localhost:5000"
client = Client(url=default_url)

result = client.flush_key(key="key")
print(result.deleted_count)
```
