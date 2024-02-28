from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.redis_hash_table, name='admin-redis-hash-table'),
    url(r'test/$', views.redis_hash_table_test, name='admin-redis-hash-table-test'),
]
