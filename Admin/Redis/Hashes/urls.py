from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.redis_hash_table, name='admin-redis-hash-table'),
    url(r'keys/$', views.redis_hash_keys, name='admin-redis-hash-keys'),
    url(r'form/$', views.redis_hash_form, name='admin-redis-hash-form'),
]
