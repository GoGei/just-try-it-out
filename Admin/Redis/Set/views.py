from django_hosts import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from core.Utils.Access.decorators import manager_required
from .forms import (
    RedisSetTableForm, RedisSetAddForm, RedisSetCardForm, RedisSetDiffForm, RedisSetInterForm
)


@manager_required
def redis_set_table(request):
    if '_refresh' in request.POST:
        return redirect(reverse('admin-redis-set-table', host='admin'))

    body = RedisSetTableForm(request.POST or None, user=request.user)
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
                return redirect(reverse('admin-redis-set-table', host='admin'))
            else:
                data = body.apply_search()
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    content = {
        'data': data,
        'form': {
            'body': body,
            'title': _('Set table'),
            'buttons': {'submit': True, 'refresh': True, 'clear': True}
        }
    }
    return render(request, 'Admin/Redis/Set/redis_set_table.html', content)


@manager_required
def redis_set_add(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-set-add', host='admin'))

    body = RedisSetAddForm(request.POST or None, user=request.user)
    sets = None
    if body.is_valid():
        try:
            result = body.add()
            msg = _(f'Add executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work(body.get_keys_on_work())

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set add'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/Set/redis_set_add.html', context)


@manager_required
def redis_set_cardinality(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-set-cardinality', host='admin'))

    body = RedisSetCardForm(request.POST or None, user=request.user)
    sets = None
    if body.is_valid():
        try:
            result = body.cardinality()
            msg = _(f'Cardinality executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work(body.get_keys_on_work())

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set cardinality'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/Set/redis_set_cardinality.html', context)


@manager_required
def redis_set_difference(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-set-difference', host='admin'))

    body = RedisSetDiffForm(request.POST or None, user=request.user)
    sets = None
    if body.is_valid():
        try:
            result = body.difference()
            msg = _(f'Difference executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work(body.get_keys_on_work())

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set difference'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/Set/redis_set_difference.html', context)


@manager_required
def redis_set_intersect(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-set-intersect', host='admin'))

    body = RedisSetInterForm(request.POST or None, user=request.user)
    sets = None
    if body.is_valid():
        try:
            result = body.intersect()
            msg = _(f'Intersect executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work(body.get_keys_on_work())

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set intersection'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/Set/redis_set_intersect.html', context)
