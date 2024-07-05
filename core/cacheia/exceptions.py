from cacheia_schemas import Backend


class KeyAlreadyExists(KeyError):
    """
    Raised when a key already exists in the cache
    """

    def __init__(self, key: str) -> None:
        self.key = key
        self.message = f"Key '{key}' already exists in the cache."
        super().__init__(self.message)


class InvalidBackend(ValueError):
    def __init__(self, backend_name: str) -> None:
        backend_names = "\n-> ".join(Backend)

        self.backend_name = backend_name
        self.message = f"Settings type '{backend_name}' is not supported. Supported backends are:\n-> {backend_names}."
        super().__init__(self.message)
