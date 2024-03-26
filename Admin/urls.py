from django.urls import re_path
from django.conf.urls import include

urlpatterns = [
    re_path('', include('urls')),
    re_path('^', include('Admin.Home.urls')),
    re_path('^', include('Admin.Login.urls')),

    re_path('^redis/', include('Admin.Redis.urls')),
    re_path('^logger/', include('Admin.Logger.urls')),
]
