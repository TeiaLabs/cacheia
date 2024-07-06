# Cacheia API

This module contains the API for the Cacheia project. It exposes a HTTP interface to interact with all cacheia functionalities.

## Installation

Install core with "core" optional to download core dependency:

```bash
pip install -e ./api[core]
```

## API Endpoints

-   <span style="color:green">**POST**</span> `/cache/`: receives the body parameter `instance: CachedValue` and creates a new cache instance in the configured backend.
-   <span style="color:blue">**GET**</span> `/cache/`: receives the optional params `group: str, expires_range: tuple[float, float], creation_range: tuple[datetime, datetime]` and gets all cached values that match the filters.
-   <span style="color:blue">**GET**</span> `/cache/{key}/`: receives the params `key: str` and gets the cached value for the given key.
-   <span style="color:orange">**DELETE**</span> `/cache/`: receives the optional params `group: str, expires_range: tuple[float, float], creation_range: tuple[datetime, datetime]` and flushes all cached values that matched the criteria.
-   <span style="color:orange">**DELETE**</span> `/cache/{key}/`: receives the param `key: str` and flushes a specific key, removing its register in application cache.
-   <span style="color:orange">**DELETE**</span> `/cache/$clear/`: receives no params and flushes all cached values in the application cache.

## Docs

Run the code locally and check-out:

-   [Iterative](http://localhost:5000/docs): for an iterative experience
-   [Redoc](http://localhost:5000/redoc): for a more detailed view

## Running the API

To run the API it is only necessary to install the `cacheia_api` (api folder) and `cacheia` (core folder) packages and run the command:

`python -m cacheia_api`

It will run a local server with reload and one worker configured by default.
