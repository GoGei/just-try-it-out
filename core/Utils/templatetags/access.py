from django import template
from core.Utils.Access.user_check_functions import manager_check, superuser_check

register = template.Library()


@register.simple_tag
def user_is_manager(request):
    user = request.user
    return manager_check(user)


@register.simple_tag
def user_is_superuser(request):
    user = request.user
    return superuser_check(user)


@register.simple_tag
def user_is_owner(request, obj, owner_field: str = 'user'):
    user = request.user
    return bool(user) and getattr(obj, owner_field) == user
