from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'login/$', views.login_view, name='admin-login'),
    re_path(r'logout/$', views.logout_view, name='admin-logout'),
]
