class KeyAlreadyExists(KeyError):
    """
    Raised when a key already exists in the cache
    """

    def __init__(self, key: str) -> None:
        self.key = key
        self.message = f"Key '{key}' already exists in the cache."
        super().__init__(self.message)


class InvalidSettings(ValueError):
    def __init__(self, backend_name: str) -> None:
        self.settings_type = backend_name
        self.message = f"Settings type '{backend_name}' is not supported."
        super().__init__(self.message)
