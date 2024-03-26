from django_hosts import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from core.Utils.Access.decorators import manager_required
from .forms import (
    RedisStringSetForm, RedisStringTableForm, RedisStringDeleteForm, RedisStringCounterForm, RedisStringGetDelForm,
    RedisStringGetRangeForm, RedisStringGetSetForm, RedisStringLCSForm
)


@manager_required
def redis_string_table(request):
    if '_refresh' in request.POST:
        return redirect(reverse('admin-redis-string-table', host='admin'))

    body = RedisStringTableForm(request.POST or None, user=request.user)
    data = body.get()
    if body.is_valid():
        try:
            if '_clear' in request.POST:
                result = body.clear()
                msg = _(f'Clean executed with result: {result}')
                if result:
                    messages.info(request, msg)
                else:
                    messages.warning(request, msg)
                return redirect(reverse('admin-redis-string-table', host='admin'))
            else:
                data = body.apply_search()
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    content = {
        'data': data,
        'form': {
            'body': body,
            'title': _('String table'),
            'buttons': {'submit': True, 'refresh': True, 'clear': True}
        }
    }
    return render(request, 'Admin/Redis/String/redis_string_table.html', content)


@manager_required
def redis_string_set(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-string-set', host='admin'))

    body = RedisStringSetForm(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.set()
            msg = _(f'Set executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisStringTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('String set'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/String/redis_string_set.html', context)


@manager_required
def redis_string_delete(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-string-delete', host='admin'))

    body = RedisStringDeleteForm(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.delete()
            msg = _(f'Delete executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisStringTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('String delete'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/String/redis_string_delete.html', context)


@manager_required
def redis_string_counter(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-string-counter', host='admin'))

    body = RedisStringCounterForm(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.execute()
            msg = _(f'Counter command executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Counter Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisStringTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('String as counter'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/String/redis_string_counter.html', context)


@manager_required
def redis_string_get_del(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-string-get-del', host='admin'))

    body = RedisStringGetDelForm(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.get_del()
            msg = _(f'GET-DEL command executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisStringTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('String GET before DEL'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/String/redis_string_get_del.html', context)


@manager_required
def redis_string_get_range(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-string-get-range', host='admin'))

    body = RedisStringGetRangeForm(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.get_range()
            msg = _(f'Get range command executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisStringTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('String get range'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/String/redis_string_get_range.html', context)


@manager_required
def redis_string_get_set(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-string-get-set', host='admin'))

    body = RedisStringGetSetForm(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.get_set()
            msg = _(f'GET-SET command executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisStringTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('String GET-SET'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/String/redis_string_get_set.html', context)


@manager_required
def redis_string_lcs(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-string-lcs', host='admin'))

    body = RedisStringLCSForm(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.lcs()
            msg = _(f'Longest common substring command executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisStringTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('Longest common substring'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/String/redis_string_lcs.html', context)
