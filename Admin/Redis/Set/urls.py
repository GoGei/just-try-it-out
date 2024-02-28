from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.redis_set_table, name='admin-redis-set-table'),
    url(r'members/$', views.redis_set_members, name='admin-redis-set-members'),
    url(r'add/$', views.redis_set_add, name='admin-redis-set-add'),
    url(r'cardinality/$', views.redis_set_cardinality, name='admin-redis-set-cardinality'),
    url(r'difference/$', views.redis_set_difference, name='admin-redis-set-difference'),
    url(r'intersect/$', views.redis_set_intersect, name='admin-redis-set-intersect'),
    url(r'intersect-cardinality/$', views.redis_set_intersect_cardinality,
        name='admin-redis-set-intersect-cardinality'),
    url(r'is-member/$', views.redis_set_is_member, name='admin-redis-set-is-member'),
    url(r'move/$', views.redis_set_move, name='admin-redis-set-move'),
    url(r'pop/$', views.redis_set_pop, name='admin-redis-set-pop'),
    url(r'rand-member/$', views.redis_set_rand_member, name='admin-redis-set-rand-member'),
    url(r'remove/$', views.redis_set_remove, name='admin-redis-set-remove'),
    url(r'union/$', views.redis_set_union, name='admin-redis-set-union'),
]
