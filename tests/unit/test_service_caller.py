import pytest

from src.services import ServiceCaller
from src.registry import AbstractServiceRegistry


class FakeRegistry(AbstractServiceRegistry):
    services = {
        'service1': 'http://service1/',
        'service2': 'http://service2',
    }

    def resolve_host(self, name: str) -> str:
        return self.services[name]


@pytest.fixture
def create_request(rf):
    def _inner(service_name, path):
        request = rf.get(path)
        request.kwargs = {'service': service_name}
        return request
    return _inner


class TestGetFullURL:

    def _get_full_url(self, request):
        caller = ServiceCaller.from_django_request(
            request,
            registry=FakeRegistry(),
        )
        return caller._get_full_url()

    def test_when_service_has_ending_slash_returns_url(
        self,
        create_request,
    ):
        request = create_request('service1', '/service1/path/')
        result = self._get_full_url(request)
        expected = 'http://service1/path/'
        assert expected == result

    def test_when_service_does_not_have_ending_slash_returns_url(
        self,
        create_request,
    ):
        request = create_request('service2', '/service2/path/')
        result = self._get_full_url(request)
        expected = 'http://service2/path/'
        assert expected == result
