# Cacheia

Cacheia is a cache abstraction that allows users to retrieve, invalidate and define expiration time to its cached values.

## Structure

The repository is separated into four subfolders:

-   api: exposes a HTTP interface for all cacheia functionalitites
-   client: a client library that can be used to interact with the cacheia API
-   core: the core library that implements the cacheia functionalities
-   middleware: a middleware that can be used alongside FastAPI to cache responses

## Docs

For more information about the modules:

-   [Checkout the API](./api/README.md)
-   [Checkout the Client](./client/README.md)
-   [Checkout the Core](./core/README.md)
-   [Checkout the Middleware](./middleware/README.md)
