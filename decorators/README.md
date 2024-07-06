# Cacheia Decorators

Exposes decorators that can be used along FastAPI and plain functions to cache responses using cacheia machinery.

## Installation

Install decorators with "schemas" optional and "local" and "remote" cache support:

```bash
pip install -e ./decorators[schemas,local,remote]
```

## Code

There are these decorators avaialble:

-   `local.cache`: which can be used on plain functions to cache values using a local cache or cacheia_client.
-   `remote.cache`: which can be used to cache values on a remote instance of cacheia (i.e. cacheia_api service).

## Usage

```python
from cacheia_decorators.local import cache as local_cache
from cacheia_decorators.remote import cache as remote_cache


@local_cache(key_builder=lambda i: str(i == 0), settings={})
def function_a():
    return "Hello World"

@remote_cache(key_builder=lambda i: str(i == 0), url="http://localhost:5000/")
def function_b():
    return "Hello World"
```
