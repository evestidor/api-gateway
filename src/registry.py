from abc import ABC, abstractmethod


class AbstractServiceRegistry(ABC):

    @abstractmethod
    def resolve_host(self, name: str) -> str:
        pass


class ServiceRegistry(AbstractServiceRegistry):
    services = {'stock-manager': 'http://evestidor-svc-stock-manager'}

    def resolve_host(self, name: str) -> str:
        return self.services[name]