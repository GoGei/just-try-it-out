from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'$', views.redis_hash_table, name='admin-redis-hash-table'),
    re_path(r'keys/$', views.redis_hash_keys, name='admin-redis-hash-keys'),
    re_path(r'info/$', views.redis_hash_info, name='admin-redis-hash-info'),
    re_path(r'form/$', views.redis_hash_form, name='admin-redis-hash-form'),
    re_path(r'random-fields/$', views.redis_hash_random_fields, name='admin-redis-hash-random-fields'),
]
