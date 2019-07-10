from django.conf import settings
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r'^{}/(?P<service>[\w\-]+)/.*'.format(settings.URL_PREFIX),
        views.GatewayView.as_view(),
    )
]
