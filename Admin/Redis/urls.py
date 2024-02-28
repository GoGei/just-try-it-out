from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'$', views.redis_index, name='admin-redis-index'),
    url(r'string/', include('Admin.Redis.String.urls')),
    url(r'list/', include('Admin.Redis.Lists.urls')),
    url(r'set/', include('Admin.Redis.Set.urls')),
    url(r'hash/', include('Admin.Redis.Hashes.urls')),
]
