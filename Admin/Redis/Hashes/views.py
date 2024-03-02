import json
from django_hosts import reverse
from django.contrib import messages
from django.http import JsonResponse
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
def redis_hash_keys(request):
    body = RedisHashTableForm(user=request.user)
    return JsonResponse(body.get(), safe=False)


@manager_required
def redis_hash_form(request):
    form_body = RedisHashForm(user=request.user)
    if request.is_ajax():
        response = {}
        status = 200
        if request.method.lower() == 'get':
            key = request.GET.get('key')
            response = form_body.get_key(key)
            if response:
                return JsonResponse(response, status=200, safe=False)

        if request.method.lower() == 'post':
            data = json.loads(request.body)
            form_body.validate_create(data)
            errors = form_body.redis_errors
            if errors:
                return JsonResponse(errors, status=400, safe=False)

            response = form_body.create(data)
            status = 201
        if request.method.lower() == 'delete':
            data = json.loads(request.body)
            response = form_body.delete(data)
            status = 200
        return JsonResponse(response, status=status, safe=False)

    context = {
        'form': {
            'body': form_body,
            'data_keys_url': reverse('admin-redis-hash-keys', host='admin'),
            'action_url': reverse('admin-redis-hash-form', host='admin'),
        }
    }
    return render(request, 'Admin/Redis/Hash/redis_hash_form.html', context)
