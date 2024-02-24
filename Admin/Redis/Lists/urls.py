from django.conf.urls import url
from . import views, constants

urlpatterns = [
    url(r'$', views.redis_list_table, name='admin-redis-list-table'),
    url(r'push/$', views.redis_list_push, name='admin-redis-list-push'),
    url(r'trim/$', views.redis_list_trim, name='admin-redis-list-trim'),
    url(r'set-rem/$', views.redis_list_set_rem, name='admin-redis-list-set-rem'),
    url(r'insert/$', views.redis_list_insert, name='admin-redis-list-insert'),
    url(r'move/$', views.redis_list_move, name='admin-redis-list-move'),
    url(r'bpop/$', views.redis_list_bpop, name='admin-redis-list-bpop'),

    url(r'queue/$', views.redis_list_structures, name='admin-redis-list-queue', kwargs={'structure': constants.QUEUE}),
    url(r'stack/$', views.redis_list_structures, name='admin-redis-list-stack', kwargs={'structure': constants.STACK}),
    url(r'deque/$', views.redis_list_structures, name='admin-redis-list-deque', kwargs={'structure': constants.DEQUE}),
    # bpush
]
