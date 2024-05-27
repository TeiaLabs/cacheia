# Cacheia CLient

This module contains a client that is responsible for communicating with the Cacheia API. It is a simple wrapper around the API endpoints, providing a more user-friendly interface for the user.

## Client Methods

* `create_cache_instance`: Takes instance (CreateRequest) and creator (Infostar) to create a new cache instance in the chosen backend.
* `get_all_cached_values`: Retrieves all cached values using creator (Infostar), with optional filters backend (Backends), expires_range (str), org_handle (str), and service_handle (str) for backend and expiration specifics.
* `get_cached_value`: Fetches the cached value associated with key (str) using creator (Infostar).
* `flush_all_keys`: Clears all keys from the cache using creator (Infostar), with an only_expired (bool) option to target only expired keys.
* `flush_specific_keys`: Flushes keys based on filters using creator (Infostar), with optional parameters backend (Backends), expires_range (str), org_handle (str), and service_handle (str) to specify which keys to flush.
* `flush_single_key`: Removes a single key from the cache and its register in the application DB and backend store using key (str) and creator (Infostar).