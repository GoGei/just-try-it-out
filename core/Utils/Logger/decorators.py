from functools import wraps
from django.utils.translation import gettext_lazy as _
from .logger import log


def admin_logger(view_func=None, log_on_status: int = 302, key: str = None, description: str = None):
    """
    Decorator to log manager actions on given status
    """
    def logger_decorator():
        def decorator(django_view):
            @wraps(django_view)
            def _wrapped_view(request, *args, **kwargs):
                response = django_view(request, *args, **kwargs)
                if response.status_code == log_on_status:
                    log.info(key or django_view.__name__,
                             description or _('Manager {manager} triggered action with args: {args}, kwargs: {kwargs}'),
                             manager=request.user.label,
                             args=str(args),
                             kwargs=str(kwargs))
                return response

            return _wrapped_view

        return decorator

    actual_decorator = logger_decorator()
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
