from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'$', views.redis_string_table, name='admin-redis-string-table'),
    re_path(r'set/$', views.redis_string_set, name='admin-redis-string-set'),
    re_path(r'delete/$', views.redis_string_delete, name='admin-redis-string-delete'),
    re_path(r'counter/$', views.redis_string_counter, name='admin-redis-string-counter'),

    re_path(r'get-del/$', views.redis_string_get_del, name='admin-redis-string-get-del'),
    re_path(r'get-range/$', views.redis_string_get_range, name='admin-redis-string-get-range'),
    re_path(r'get-set/$', views.redis_string_get_set, name='admin-redis-string-get-set'),
    re_path(r'lcs/$', views.redis_string_lcs, name='admin-redis-string-lcs'),
]
