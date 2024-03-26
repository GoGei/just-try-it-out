from django.urls import re_path
from django.conf.urls import include

urlpatterns = [
    re_path('', include('urls')),
    re_path('^', include('Public.Home.urls')),
]
