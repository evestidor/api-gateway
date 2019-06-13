from rest_framework.response import Response
from rest_framework.views import APIView

from .services import (
    ServiceCaller,
    ServiceError,
)


class GatewayView(APIView):

    def get(self, *args, **kwargs):
        return self._request('get')

    def post(self, *args, **kwargs):
        return self._request('post')

    def put(self, *args, **kwargs):
        return self._request('put')

    def patch(self, *args, **kwargs):
        return self._request('patch')

    def delete(self, *args, **kwargs):
        return self._request('delete')

    def _request(self, method: str) -> Response:
        try:
            fn = getattr(self._service, method)
            result = fn()
            return Response(result)
        except ServiceError as e:
            return Response(e.data, status=e.status)

    @property
    def _service(self):
        return ServiceCaller.from_django_request(
            self.request,
            self.kwargs['service'],
        )
