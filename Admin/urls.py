from django.conf.urls import include, url

urlpatterns = [
    url('', include('urls')),
    url('^', include('Admin.Home.urls')),
    url('^', include('Admin.Login.urls')),
]
