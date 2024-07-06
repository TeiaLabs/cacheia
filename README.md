# Cacheia

Cacheia is a cache abstraction that allows users to retrieve, invalidate and define expiration time to its cached values.

## Structure

The repository is separated into five subfolders:

-   api: exposes a HTTP interface for all cacheia functionalitites
-   client: a client library that can be used to interact with the cacheia API
-   core: the core library that implements the cacheia functionalities
-   decorators: helper decorators that can be used whithin FastAPI or plain functions to cache responses
-   schemas: schemas used by the API and the client

## Docs

For more information about the modules:

-   [Checkout the API](./api/README.md)
-   [Checkout the Client](./client/README.md)
-   [Checkout the Core](./core/README.md)
-   [Checkout the Schemas](./schemas/README.md)

## Install packages

Use the command below to install all packages in development mode:

```bash
pip install -e ./schemas \
    -e ./core \
    -e ./decorators \
    -e ./client \
    -e ./api
```
