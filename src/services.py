from abc import ABC, abstractmethod
from os.path import join

import requests
from django.http.request import HttpRequest

from .registry import ServiceRegistry


class Response(ABC):

    @abstractmethod
    def json(self) -> dict:
        pass


class RequestHandler(ABC):

    @abstractmethod
    def get(self, url: str, params: dict = None) -> Response:
        pass

    @abstractmethod
    def post(self, url: str, json: dict = None) -> Response:
        pass

    @abstractmethod
    def put(self, url: str, json: dict = None) -> Response:
        pass

    @abstractmethod
    def patch(self, url: str, json: dict = None) -> Response:
        pass

    @abstractmethod
    def delete(self, url: str) -> Response:
        pass


class Request:

    def __init__(
        self,
        path: str,
        service_name: str,
        data: dict = None,
    ):
        self.path = self._remove_service_from_path(path, service_name)
        self.service_name = service_name
        self.data = data or {}

    @classmethod
    def from_django_request(cls, request: HttpRequest):
        data = {}
        data.update(request.GET)
        data.update(request.POST)
        return cls(
            path=request.path,
            service_name=request.kwargs['service'],
            data=data,
        )

    @staticmethod
    def _remove_service_from_path(path: str, service_name: str) -> str:
        path = path.replace(service_name, '')
        path = path.replace('//', '')
        return path


class ServiceCaller:

    def __init__(
        self,
        request: Request,
        request_handler: RequestHandler = None,
        registry: ServiceRegistry = None,
    ):
        self._request = request
        self._request_handler = request_handler or requests
        self._registry = registry or ServiceRegistry()

    @classmethod
    def from_django_request(
        cls,
        request: HttpRequest,
        request_handler: RequestHandler = None,
        registry: ServiceRegistry = None,
    ):
        request = Request.from_django_request(request)
        return cls(request, request_handler, registry)

    def get(self):
        response = self._request_handler.get(
            self._get_full_url(),
            params=self._request.data,
        )
        return response.json()

    def post(self):
        response = self._request_handler.post(
            self._get_full_url(),
            data=self._request.data,
        )
        return response.json()

    def patch(self):
        response = self._request_handler.patch(
            self._get_full_url(),
            data=self._request.data,
        )
        return response.json()

    def put(self):
        response = self._request_handler.put(
            self._get_full_url(),
            data=self._request.data,
        )
        return response.json()

    def delete(self):
        url = self._get_full_url()
        response = self._request_handler.delete(url)
        return response.json()

    def _get_full_url(self) -> str:
        service_name = self._request.service_name
        service_host = self._registry.resolve_host(service_name)
        return join(service_host, self._request.path)
