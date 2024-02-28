from django_hosts import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from core.Utils.Access.decorators import manager_required
from .forms import (
    RedisSetTableForm, RedisSetAddForm, RedisSetCardForm, RedisSetDiffForm, RedisSetInterForm, RedisSetMembersForm,
    RedisSetInterCardForm, RedisSetIsMemberForm, RedisSetMoveForm, RedisSetPopForm, RedisSetRandMemberForm,
    RedisSetRemoveForm, RedisSetUnionForm
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
                messages.info(request, msg)
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
def redis_set_members(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-set-get', host='admin'))

    body = RedisSetMembersForm(request.POST or None, user=request.user)
    sets = None
    if body.is_valid():
        try:
            result = body.members()
            msg = _(f'Get executed with result: {result}')
            messages.info(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work()

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set members'),
            'buttons': {'submit': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/Set/redis_set_members.html', context)


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
            messages.info(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work()

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set add'),
            'buttons': {'submit': True, 'cancel': True}
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
            messages.info(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work()

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set cardinality'),
            'buttons': {'submit': True, 'cancel': True}
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
            messages.info(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work()

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set difference'),
            'buttons': {'submit': True, 'cancel': True}
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
            messages.info(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work()

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set intersection'),
            'buttons': {'submit': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/Set/redis_set_intersect.html', context)


@manager_required
def redis_set_intersect_cardinality(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-set-intersect-cardinality', host='admin'))

    body = RedisSetInterCardForm(request.POST or None, user=request.user)
    sets = None
    if body.is_valid():
        try:
            result = body.intersect_cardinality()
            msg = _(f'Intersect cardinality executed with result: {result}')
            messages.info(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work()

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set intersect cardinality'),
            'buttons': {'submit': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/Set/redis_set_intersect_cardinality.html', context)


@manager_required
def redis_set_is_member(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-set-is-member', host='admin'))

    body = RedisSetIsMemberForm(request.POST or None, user=request.user)
    sets = None
    if body.is_valid():
        try:
            result = body.ismember()
            msg = _(f'Is member with result: {result}')
            messages.info(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work()

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set is member'),
            'buttons': {'submit': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/Set/redis_set_is_member.html', context)


@manager_required
def redis_set_move(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-set-move', host='admin'))

    body = RedisSetMoveForm(request.POST or None, user=request.user)
    sets = None
    if body.is_valid():
        try:
            result = body.move()
            msg = _(f'Move executed with result: {result}')
            messages.info(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work()

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set move'),
            'buttons': {'submit': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/Set/redis_set_move.html', context)


@manager_required
def redis_set_pop(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-set-pop', host='admin'))

    body = RedisSetPopForm(request.POST or None, user=request.user)
    sets = None
    if body.is_valid():
        try:
            result = body.pop()
            msg = _(f'Pop executed with result: {result}')
            messages.info(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work()

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set pop'),
            'buttons': {'submit': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/Set/redis_set_pop.html', context)


@manager_required
def redis_set_rand_member(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-set-rand-member', host='admin'))

    body = RedisSetRandMemberForm(request.POST or None, user=request.user)
    sets = None
    if body.is_valid():
        try:
            result = body.rand_member()
            msg = _(f'Rand member executed with result: {result}')
            messages.info(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work()

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set rand member'),
            'buttons': {'submit': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/Set/redis_set_rand_member.html', context)


@manager_required
def redis_set_remove(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-set-remove', host='admin'))

    body = RedisSetRemoveForm(request.POST or None, user=request.user)
    sets = None
    if body.is_valid():
        try:
            result = body.remove()
            msg = _(f'Remove executed with result: {result}')
            messages.info(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work()

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set remove'),
            'buttons': {'submit': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/Set/redis_set_remove.html', context)


@manager_required
def redis_set_union(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-set-union', host='admin'))

    body = RedisSetUnionForm(request.POST or None, user=request.user)
    sets = None
    if body.is_valid():
        try:
            result = body.union()
            msg = _(f'Union executed with result: {result}')
            messages.info(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)
        sets = body.get_sets_on_work()

    context = {
        'sets': sets,
        'form': {
            'body': body,
            'title': _('Set union'),
            'buttons': {'submit': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/Set/redis_set_union.html', context)
