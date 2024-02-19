from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'login/$', views.login_view, name='admin-login'),
    url(r'logout/$', views.logout_view, name='admin-logout'),
]
