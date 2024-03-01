import json
from django_hosts import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from core.Utils.Access.decorators import manager_required
from .forms import (
    RedisHashTableForm, RedisHashForm
)


@manager_required
def redis_hash_table(request):
    if '_refresh' in request.POST:
        return redirect(reverse('admin-redis-hash-table', host='admin'))

    body = RedisHashTableForm(request.POST or None, user=request.user)
    data = body.get()
    if body.is_valid():
        try:
            if '_clear' in request.POST:
                result = body.clear()
                msg = _(f'Clean executed with result: {result}')
                messages.info(request, msg)
                return redirect(reverse('admin-redis-hash-table', host='admin'))
            else:
                data = body.apply_search()
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    content = {
        'data': data,
        'form': {
            'body': body,
            'title': _('Hash table'),
            'buttons': {'submit': True, 'refresh': True, 'clear': True}
        }
    }
    return render(request, 'Admin/Redis/Hash/redis_hash_table.html', content)


@manager_required
def redis_hash_form(request):
    form_body = RedisHashForm(user=request.user)
    if request.is_ajax():
        data = json.loads(request.body)

        response = None
        if request.method.lower() == 'post':
            response = form_body.create(data)
        if request.method.lower() == 'delete':
            response = form_body.delete(data)
        print(response)

    context = {
        'form': {
            'body': form_body,
            'action_url': reverse('admin-redis-hash-form', host='admin'),
        }
    }
    return render(request, 'Admin/Redis/Hash/redis_hash_form.html', context)
