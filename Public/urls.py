from django.conf.urls import include, url

urlpatterns = [
    url('', include('urls')),
    url('^', include('Public.Home.urls')),
]
