from rest_framework.views import APIView

from .services import ServiceCaller


class GatewayView(APIView):

    def get(self, request, *args, **kwargs):
        return ServiceCaller.from_django_request(request).get()

    def post(self, request, *args, **kwargs):
        return ServiceCaller.from_django_request(request).post()

    def put(self, request, *args, **kwargs):
        return ServiceCaller.from_django_request(request).put()

    def patch(self, request, *args, **kwargs):
        return ServiceCaller.from_django_request(request).patch()

    def delete(self, request, *args, **kwargs):
        return ServiceCaller.from_django_request(request).delete()
