from cacheia_schemas import Backend


class KeyAlreadyExists(KeyError):
    """
    Raised when a key already exists in the cache
    """

    def __init__(self, key: str) -> None:
        self.key = key
        self.message = f"Key '{key}' already exists in the cache"
        super().__init__(self.message)


class InvalidExpireRange(ValueError):
    """
    Raised when the expire range is not valid
    """

    def __init__(self, expires_range: str) -> None:
        self.expire = expires_range
        self.message = f"Expire value '{expires_range}' is not a valid range, a valid format is '<start>...<end>' where 'end' is greater than 'start'."
        super().__init__(self.message)


class InvalidBackendName(ValueError):
    def __init__(self, backend_name: str) -> None:
        backend_names = "\n-> ".join(Backend)

        self.backend_name = backend_name
        self.message = f"Backend name '{backend_name}' is not a valid backend name. Valid names are:\n-> {backend_names}"
        super().__init__(self.message)
