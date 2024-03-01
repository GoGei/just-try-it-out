from django.conf import settings


def default_context(request):
    return {
        'SITE_URL': settings.SITE_URL,
        'SITE_SCHEME': settings.SITE_SCHEME,
        'PARENT_HOST': settings.PARENT_HOST,
        'HOST_PORT': settings.HOST_PORT,
    }
