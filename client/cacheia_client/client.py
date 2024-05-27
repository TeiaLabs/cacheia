def create_cache_instance(instance: CreateRequest, creator: Infostar):
    """
    Creates a new cache instance in the chosen backend.
    """
    return Client().create_cache_instance(instance=instance, creator=creator)


def get_all_cached_values(
    creator: Infostar,
    backend: Optional[Backends] = None,
    expires_range: Optional[str] = None,
    org_handle: Optional[str] = None,
    service_handle: Optional[str] = None,
):
    """
    Gets all cached values for the given backend and filters by the given parameters.
    """
    return Client().get_all_cached_values(
        creator=creator,
        backend=backend,
        expires_range=expires_range,
        org_handle=org_handle,
        service_handle=service_handle,
    )


def get_cached_value(key: str, creator: Infostar):
    """
    Gets the cached value for the given key.
    """
    return Client().get_cached_value(key=key, creator=creator)


def flush_all_keys(creator: Infostar, only_expired: bool):
    """
    Flushes all keys in the cache, removing all registers in application DB and backend store.
    Optionally accepts a flag that indicates if it should only flush expired keys.
    """
    return Client().flush_all_keys(creator=creator, only_expired=only_expired)


def flush_specific_keys(
    creator: Infostar,
    backend: Optional[Backends] = None,
    expires_range: Optional[str] = None,
    org_handle: Optional[str] = None,
    service_handle: Optional[str] = None,
):
    """
    Flushes specific keys based on the given parameters.
    """
    return Client().flush_specific_keys(
        creator=creator,
        backend=backend,
        expires_range=expires_range,
        org_handle=org_handle,
        service_handle=service_handle,
    )


def flush_single_key(key: str, creator: Infostar):
    """
    Flushes a specific key, removing its register in application DB and backend store.
    """
    return Client().flush_single_key(key=key, creator=creator)


class Client:
    def create_cache_instance(self, instance: CreateRequest, creator: Infostar):
        """
        Creates a new cache instance in the chosen backend.
        """
        pass

    def get_all_cached_values(
        self,
        creator: Infostar,
        backend: Optional[Backends] = None,
        expires_range: Optional[str] = None,
        org_handle: Optional[str] = None,
        service_handle: Optional[str] = None,
    ):
        """
        Gets all cached values for the given backend and filters by the given parameters.
        """
        pass

    def get_cached_value(self, key: str, creator: Infostar):
        """
        Gets the cached value for the given key.
        """
        pass

    def flush_all_keys(self, creator: Infostar, only_expired: bool):
        """
        Flushes all keys in the cache, removing all registers in application DB and backend store.
        Optionally accepts a flag that indicates if it should only flush expired keys.
        """
        pass

    def flush_specific_keys(
        self,
        creator: Infostar,
        backend: Optional[Backends] = None,
        expires_range: Optional[str] = None,
        org_handle: Optional[str] = None,
        service_handle: Optional[str] = None,
    ):
        """
        Flushes specific keys based on the given parameters.
        """
        pass

    def flush_single_key(self, key: str, creator: Infostar):
        """
        Flushes a specific key, removing its register in application DB and backend store.
        """
        pass
