from django_hosts import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from core.Utils.Access.decorators import manager_required
from .forms import RedisStringSetForm


@manager_required
def redis_index(request):
    return render(request, 'Admin/Redis/redis_index.html')


@manager_required
def redis_string(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-string', host='admin'))

    form_data = request.POST or {}
    if '_refresh' in request.POST:
        form_data = {}

    body = RedisStringSetForm(form_data or None, user=request.user)
    data = body.get()

    if body.is_valid():
        result = body.set()
        msg = _(f'Set executed with result: {result}')
        if result:
            messages.info(request, msg)
        else:
            messages.warning(request, msg)
        return redirect(reverse('admin-redis-string', host='admin'))

    form = {
        'body': body,
        'buttons': {'save': True, 'cancel': True, 'refresh': True},
    }
    return render(request, 'Admin/Redis/redis_string.html', {'form': form, 'data': data})
