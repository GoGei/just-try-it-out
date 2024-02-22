from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.redis_list_table, name='admin-redis-list-table'),
    url(r'push/$', views.redis_list_push, name='admin-redis-list-push'),
    url(r'trim/$', views.redis_list_trim, name='admin-redis-list-trim'),
    url(r'set-rem/$', views.redis_list_set_rem, name='admin-redis-list-set-rem'),
    url(r'insert/$', views.redis_list_insert, name='admin-redis-list-insert'),
    # bpush
]
