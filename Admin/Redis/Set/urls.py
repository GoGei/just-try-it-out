from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', views.redis_set_table, name='admin-redis-set-table'),
    url(r'add/$', views.redis_set_add, name='admin-redis-set-add'),
    url(r'cardinality/$', views.redis_set_cardinality, name='admin-redis-set-cardinality'),
    url(r'difference/$', views.redis_set_difference, name='admin-redis-set-difference'),
    url(r'intersect/$', views.redis_set_intersect, name='admin-redis-set-intersect'),
]
