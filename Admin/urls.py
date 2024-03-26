from django.conf.urls import include, url

urlpatterns = [
    url('', include('urls')),
    url('^', include('Admin.Home.urls')),
    url('^', include('Admin.Login.urls')),

    url('^redis/', include('Admin.Redis.urls')),
    url('^logger/', include('Admin.Logger.urls')),
]
