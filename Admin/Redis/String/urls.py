from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.redis_string_table, name='admin-redis-string-table'),
    url(r'set/$', views.redis_string_set, name='admin-redis-string-set'),
    url(r'delete/$', views.redis_string_delete, name='admin-redis-string-delete'),
    url(r'counter/$', views.redis_string_counter, name='admin-redis-string-counter'),
]
