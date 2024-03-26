from django.urls import re_path
from django.conf.urls import include
from . import views

urlpatterns = [
    re_path(r'$', views.redis_index, name='admin-redis-index'),
    re_path(r'string/', include('Admin.Redis.String.urls')),
    re_path(r'list/', include('Admin.Redis.Lists.urls')),
    re_path(r'set/', include('Admin.Redis.Set.urls')),
    re_path(r'hash/', include('Admin.Redis.Hashes.urls')),
]
