from rest_framework.views import APIView


class GatewayCaller:

    def __init__(self, request):
        self._request = request

    def get(self):
        service_name = ''
        self._request.get('svc-stock-manager')


class GatewayView(APIView):

    def get(self, request, *args, **kwargs):
        return GatewayCaller(request).get()

    def post(self, request, *args, **kwargs):
        return

    def put(self, request, *args, **kwargs):
        return

    def patch(self, request, *args, **kwargs):
        return

    def delete(self, request, *args, **kwargs):
        return
