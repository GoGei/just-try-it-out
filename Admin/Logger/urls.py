from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'$', views.activity_log_list, name='admin-logger-list'),
    re_path(r'objects/$', views.activity_log_objects_list, name='admin-logger-objects-list'),

    re_path(r'^trigger/$', views.admin_logger_trigger, name='admin-logger-trigger'),
    re_path(r'^trigger/with-error/$', views.admin_logger_trigger_with_error, name='admin-logger-trigger-with-error'),
    re_path(r'^trigger/(?P<some_int>\d+)/(?P<slug>[\w-]+)/$', views.admin_logger_trigger_params,
            name='admin-logger-trigger-params'),
]
