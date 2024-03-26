from django.urls import re_path
from . import views, constants

urlpatterns = [
    re_path(r'$', views.redis_list_table, name='admin-redis-list-table'),
    re_path(r'push/$', views.redis_list_push, name='admin-redis-list-push'),
    re_path(r'trim/$', views.redis_list_trim, name='admin-redis-list-trim'),
    re_path(r'set-rem/$', views.redis_list_set_rem, name='admin-redis-list-set-rem'),
    re_path(r'insert/$', views.redis_list_insert, name='admin-redis-list-insert'),
    re_path(r'move/$', views.redis_list_move, name='admin-redis-list-move'),
    re_path(r'bpop/$', views.redis_list_bpop, name='admin-redis-list-bpop'),
    re_path(r'blmpop/$', views.redis_list_blmpop, name='admin-redis-list-blmpop'),

    re_path(r'queue/$', views.redis_list_structures, name='admin-redis-list-queue',
            kwargs={'structure': constants.QUEUE}),
    re_path(r'stack/$', views.redis_list_structures, name='admin-redis-list-stack',
            kwargs={'structure': constants.STACK}),
    re_path(r'deque/$', views.redis_list_structures, name='admin-redis-list-deque',
            kwargs={'structure': constants.DEQUE}),
]
