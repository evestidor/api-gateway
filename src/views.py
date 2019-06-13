from rest_framework.views import APIView

from .services import ServiceCaller


class GatewayView(APIView):

    def get(self, *args, **kwargs):
        return self._service.get()

    def post(self, *args, **kwargs):
        return self._service.post()

    def put(self, *args, **kwargs):
        return self._service.put()

    def patch(self, *args, **kwargs):
        return self._service.patch()

    def delete(self, *args, **kwargs):
        return self._service.delete()

    @property
    def _service(self):
        return ServiceCaller.from_django_request(
            self.request,
            self.kwargs['service'],
        )
