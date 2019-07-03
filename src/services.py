from abc import ABC, abstractmethod
from os.path import join
from json.decoder import JSONDecodeError

import requests
from rest_framework.request import Request as RFRequest

from .registry import ServiceRegistry


class ServiceError(Exception):
    def __init__(
        self,
        data: dict,
        status: int,
    ):
        self.data = data
        self.status = status


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
        query_params: dict = None,
        data: dict = None,
    ):
        self.path = self._remove_service_from_path(path, service_name)
        self.service_name = service_name
        self.query_params = query_params or {}
        self.data = data or {}

    @staticmethod
    def _remove_service_from_path(path: str, service_name: str) -> str:
        path = path.replace(service_name, '')
        path = path.replace('//', '')
        if not path.endswith('/'):
            path += '/'
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
        request: RFRequest,
        service_name: str,
        request_handler: RequestHandler = None,
        registry: ServiceRegistry = None,
    ):
        request = Request(
            path=request.path,
            service_name=service_name,
            query_params=request.query_params,
            data=request.data,
        )
        return cls(request, request_handler, registry)

    def get(self):
        response = self._request_handler.get(
            self._get_full_url(),
            params=self._request.query_params,
        )
        return self._parse_response(response)

    def post(self):
        response = self._request_handler.post(
            self._get_full_url(),
            data=self._request.data,
            params=self._request.query_params,
        )
        return self._parse_response(response)

    def patch(self):
        response = self._request_handler.patch(
            self._get_full_url(),
            data=self._request.data,
            params=self._request.query_params,
        )
        return self._parse_response(response)

    def put(self):
        response = self._request_handler.put(
            self._get_full_url(),
            data=self._request.data,
            params=self._request.query_params,
        )
        return self._parse_response(response)

    def delete(self):
        url = self._get_full_url()
        response = self._request_handler.delete(url)
        return self._parse_response(response)

    def _get_full_url(self) -> str:
        service_name = self._request.service_name
        service_host = self._registry.resolve_host(service_name)
        return join(service_host, self._request.path)

    def _parse_response(self, response):
        try:
            result = response.json()
        except JSONDecodeError:
            raise ServiceError({}, status=500)

        if response.ok:
            return result
        else:
            raise ServiceError(result, response.status_code)
