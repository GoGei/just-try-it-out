from django.urls import re_path
from django.conf import settings
from django.conf.urls import include

from .routers import router_v1, documentation

app_name = 'api'

urlpatterns = [
    re_path(r'^', include('urls')),
    re_path(r'^', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^v1/', include((router_v1.router_v1.urls, 'api'), namespace='api-v1')),
]

if settings.API_DOCUMENTATION:
    urlpatterns += documentation.urlpatterns
