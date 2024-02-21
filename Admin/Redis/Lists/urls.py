from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.redis_list_table, name='admin-redis-list-table'),
    url(r'push/$', views.redis_list_push, name='admin-redis-list-push'),
]
