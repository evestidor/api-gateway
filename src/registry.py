from abc import ABC, abstractmethod
from django.conf import settings


class AbstractServiceRegistry(ABC):

    @abstractmethod
    def resolve_host(self, name: str) -> str:
        pass


class ServiceRegistry(AbstractServiceRegistry):
    services = {'stock-manager': settings.STOCK_MANAGER_URL}

    def resolve_host(self, name: str) -> str:
        return self.services[name]
