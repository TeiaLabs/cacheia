from abc import ABC, abstractmethod



class CacheClient(ABC):
    @abstractmethod
    def create_cache_instance(self, instance, creator):
        raise NotImplementedError()

    @abstractmethod
    def get_all_cached_values(
        self,
        creator,
        backend=None,
        expires_range=None,
        org_handle=None,
        service_handle=None,
    ):
        raise NotImplementedError()

    @abstractmethod
    def get_cached_value(self, key, creator):
        raise NotImplementedError()

    @abstractmethod
    def flush_all_keys(self, creator, only_expired=False):
        raise NotImplementedError()

    @abstractmethod
    def flush_specific_keys(
        self,
        creator,
        backend=None,
        expires_range=None,
        org_handle=None,
        service_handle=None,
    ):
        raise NotImplementedError()

    @abstractmethod
    def flush_single_key(self, key, creator):
        raise NotImplementedError()
