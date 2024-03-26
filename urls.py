from django.urls import re_path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from ckeditor_uploader.views import upload


urlpatterns = [
    re_path(r'^ckeditor/upload/', login_required(upload), name='ckeditor_upload'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG and settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += [
        re_path('^__debug__/', include(debug_toolbar.urls)),
    ]
