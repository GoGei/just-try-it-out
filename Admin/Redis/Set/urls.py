from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'$', views.redis_set_table, name='admin-redis-set-table'),
    re_path(r'members/$', views.redis_set_members, name='admin-redis-set-members'),
    re_path(r'add/$', views.redis_set_add, name='admin-redis-set-add'),
    re_path(r'cardinality/$', views.redis_set_cardinality, name='admin-redis-set-cardinality'),
    re_path(r'difference/$', views.redis_set_difference, name='admin-redis-set-difference'),
    re_path(r'intersect/$', views.redis_set_intersect, name='admin-redis-set-intersect'),
    re_path(r'intersect-cardinality/$', views.redis_set_intersect_cardinality,
        name='admin-redis-set-intersect-cardinality'),
    re_path(r'is-member/$', views.redis_set_is_member, name='admin-redis-set-is-member'),
    re_path(r'move/$', views.redis_set_move, name='admin-redis-set-move'),
    re_path(r'pop/$', views.redis_set_pop, name='admin-redis-set-pop'),
    re_path(r'rand-member/$', views.redis_set_rand_member, name='admin-redis-set-rand-member'),
    re_path(r'remove/$', views.redis_set_remove, name='admin-redis-set-remove'),
    re_path(r'union/$', views.redis_set_union, name='admin-redis-set-union'),
]
