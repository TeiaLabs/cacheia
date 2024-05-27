# Cacheia API

This module contains the API for the Cacheia project. It exposes a HTTP interface to interact with all cacheia functionalities.

## API Endpoints

-   <span style="color:green">**POST**</span> `/`: receives the params `instance: CreateRequest, creator: Infostar` and creates a new cache instance in the chosen backend (e.g. redis, mongo, or memory).
-   <span style="color:blue">**GET**</span> `/`: receives the params `creator: Infostar, backend: Backends | None, expires_range: str | None, org_handle: str | None, service_handle: str | None` and gets all cached values for the given backend and filters by the given parameters.
-   <span style="color:blue">**GET**</span> `/{key}/`: receives the params `key: str, creator: Infostar` and gets the cached value for the given key.
-   <span style="color:orange">**PUT**</span> `/all/`: receives the params `creator: Infostar, only_expired: bool` and flushes all keys in the cache, removing all registers in application DB and backend store. Optionally accepts a flag that indicates if it should only flush expired keys.
-   <span style="color:orange">**PUT**</span> `/keys/`: receives the params `creator: Infostar, backend: Backends | None, expires_range: str | None, org_handle: str | None, service_handle: str | None` and flushes specific keys based on the given parameters.
-   <span style="color:orange">**PUT**</span> `/{key}/`: receives the params `key: str, creator: Infostar` and flushes a specific key, removing its register in application DB and backend store.
