# Cacheia CLient

This module contains a client that is responsible for communicating with the Cacheia API. It is a simple wrapper around the API endpoints, providing a more user-friendly interface for the user.

## Client Methods

-   `cache`: Takes instance (CreateRequest), creator (Infostar) and backend to create a new cache instance in the provided backend.
-   `get_all`: Retrieves all cached values using creator (Infostar), with optional filters backend (Backend), expires_range (str), org_handle (str), and service_handle (str) for backend and expiration specifics.
-   `get`: Fetches the cached value associated with key (str) using creator (Infostar).
-   `flush_all`: Clears all keys from the cache using creator (Infostar), with an only_expired (bool) option to target only expired keys.
-   `flush_some`: Flushes keys based on filters using creator (Infostar), with optional parameters backend (Backend), expires_range (str), org_handle (str), and service_handle (str) to specify which keys to flush.
-   `flush_key`: Removes a single key from the cache and its register in the application DB and backend store using key (str) and creator (Infostar).

## Code

The library exposes single functions that are similar to `requests` and `httpx` and also exposes a `Client` class that can be used to define default values for backend and cache API URL.

## Examples

To create a cache instance with the client:

```python
from cacheia_client import Client
from cacheia_schemas import Backend, Infostar, NewCachedValue


default_backend: Backend | None = Backend.MEMORY
default_url: str | None = "http://localhost:5000"


client = Client(backend=default_backend, url=default_url)

creator = Infostar(org_handle="handle", service_handle="handle")
instance = NewCachedValue(key="key", value="value")

# Since we are not passing "backend" it will use the default one defined in the Client
client.cache(creator=creator, instance=instance)
```

Or using the helper functions:

```python
from cacheia_client import cache, configure
from cacheia_schemas import Backend, Infostar, NewCachedValue


configure("http://localhost:5000")

creator = Infostar(org_handle="handle", service_handle="handle")
instance = NewCachedValue(key="key", value="value")
cache(creator=creator, instance=instance, backend=Backend.MEMORY)
```

Notice that when calling directly the functions, it is necessary to call "configure"
with the desired URL. Otherwise, it will fail.

---

To get all cached values:

```python
from cacheia_client import Client
from cacheia_schemas import Backend, Infostar


default_backend: Backend | None = Backend.MEMORY
default_url: str | None = "http://localhost:5000"

client = Client(backend=default_backend, url=default_url)

creator = Infostar(org_handle="handle", service_handle="handle")
for v in client.get_all(creator=creator):
    print(v)
```

---

To get a single cached value:

```python
from cacheia_client import Client
from cacheia_schemas import Backend, Infostar


default_backend: Backend | None = Backend.MEMORY
default_url: str | None = "http://localhost:5000"

client = Client(backend=default_backend, url=default_url)

creator = Infostar(org_handle="handle", service_handle="handle")
print(client.get(creator=creator, key="key"))
```

---

To flush all keys:

```python
from cacheia_client import Client
from cacheia_schemas import Backend, Infostar


default_backend: Backend | None = Backend.MEMORY
default_url: str | None = "http://localhost:5000"

client = Client(backend=default_backend, url=default_url)

creator = Infostar(org_handle="handle", service_handle="handle")
result = client.flush_all(creator=creator)
print(result.deleted_count)
```

---

To flush some keys:

```python
from datetime import datetime
from cacheia_client import Client
from cacheia_schemas import Backend, Infostar


default_backend: Backend | None = Backend.MEMORY
default_url: str | None = "http://localhost:5000"

client = Client(backend=default_backend, url=default_url)
creator = Infostar(org_handle="handle", service_handle="handle")

now = datetime.now().timestamp()
result = client.flush_some(creator=creator, backend=Backend.MEMORY, expires_range=f"{now-10}...{now+10}")
print(result.deleted_count)
```

---

To flush a single key:

```python
from cacheia_client import Client
from cacheia_schemas import Backend, Infostar


default_backend: Backend | None = Backend.MEMORY
default_url: str | None = "http://localhost:5000"

client = Client(backend=default_backend, url=default_url)

creator = Infostar(org_handle="handle", service_handle="handle")
result = client.flush_key(creator=creator, key="key")
print(result.deleted_count)
```
