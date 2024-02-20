from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'$', views.redis_index, name='admin-redis-index'),
    url(r'string/', include('Admin.Redis.String.urls')),
]
