from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.redis_index, name='admin-redis-index'),
    url(r'string/$', views.redis_string, name='admin-redis-string'),
]
