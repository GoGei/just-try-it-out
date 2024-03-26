from django_hosts import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from core.Utils.Access.decorators import manager_required
from .forms import (
    RedisListTableForm, RedisListPushForm, RedisListTrimForm, RedisListSetRemForm, RedisListInsertForm,
    RedisListMoveForm, RedisListQueueForm, RedisListDequeForm, RedisListStackForm, RedisListBlockPopForm,
    RedisListBLMPopForm
)
from . import constants


@manager_required
def redis_list_table(request):
    if '_refresh' in request.POST:
        return redirect(reverse('admin-redis-list-table', host='admin'))

    body = RedisListTableForm(request.POST or None, user=request.user)
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
                return redirect(reverse('admin-redis-list-table', host='admin'))
            else:
                data = body.apply_search()
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    content = {
        'data': data,
        'form': {
            'body': body,
            'title': _('Lists table'),
            'buttons': {'submit': True, 'refresh': True, 'clear': True}
        }
    }
    return render(request, 'Admin/Redis/List/redis_list_table.html', content)


@manager_required
def redis_list_push(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-list-push', host='admin'))

    body = RedisListPushForm(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.push()
            msg = _(f'Push executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisListTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('List push'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/List/redis_list_push.html', context)


@manager_required
def redis_list_trim(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-list-trim', host='admin'))

    body = RedisListTrimForm(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.trim()
            msg = _(f'Trim executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisListTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('List trim'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/List/redis_list_trim.html', context)


@manager_required
def redis_list_set_rem(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-list-set-rem', host='admin'))

    body = RedisListSetRemForm(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.execute()
            msg = _(f'Set/Rem executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisListTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('List set/rem'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/List/redis_list_set_rem.html', context)


@manager_required
def redis_list_insert(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-list-insert', host='admin'))

    body = RedisListInsertForm(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.insert()
            msg = _(f'Insert executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisListTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('List insert'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/List/redis_list_insert.html', context)


@manager_required
def redis_list_move(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-list-move', host='admin'))

    body = RedisListMoveForm(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.move()
            msg = _(f'Move executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisListTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('List move'),
            'buttons': {'save': True, 'cancel': True}
        }
    }
    return render(request, 'Admin/Redis/List/redis_list_move.html', context)


@manager_required
def redis_list_structures(request, structure: str):
    if '_cancel' in request.POST:
        mapping = {
            constants.QUEUE: 'admin-redis-list-queue',
            constants.DEQUE: 'admin-redis-list-deque',
            constants.STACK: 'admin-redis-list-stack',
        }
        return redirect(reverse(mapping.get(structure), host='admin'))

    mapping = {
        constants.QUEUE: RedisListQueueForm,
        constants.DEQUE: RedisListDequeForm,
        constants.STACK: RedisListStackForm,
    }
    form_class = mapping.get(structure)
    body = form_class(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.execute(form_class.get_first_key_with_prefix(request.POST))
            msg = _(f'Command executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisListTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('Structure'),
            'buttons': {'custom': form_class.CUSTOM_BUTTONS},
        }
    }

    template_mapping = {
        constants.QUEUE: 'Admin/Redis/List/structure/redis_list_queue.html',
        constants.DEQUE: 'Admin/Redis/List/structure/redis_list_deque.html',
        constants.STACK: 'Admin/Redis/List/structure/redis_list_stack.html',
    }
    return render(request, template_mapping.get(structure), context)


@manager_required
def redis_list_bpop(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-list-bpop', host='admin'))

    body = RedisListBlockPopForm(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.execute(body.get_first_key_with_prefix(request.POST))
            if isinstance(result, tuple):
                raw_key, value = result
                key = body.clean_key_from_base_key(raw_key)
                result = f'{key}={value}'
            msg = _(f'Command executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisListTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('Block pop'),
            'buttons': {'cancel': True, 'custom': body.CUSTOM_BUTTONS},
        }
    }

    return render(request, 'Admin/Redis/List/redis_list_bpop.html', context)


@manager_required
def redis_list_blmpop(request):
    if '_cancel' in request.POST:
        return redirect(reverse('admin-redis-list-blmpop', host='admin'))

    body = RedisListBLMPopForm(request.POST or None, user=request.user)
    if body.is_valid():
        try:
            result = body.blmpop()
            msg = _(f'Command executed with result: {result}')
            if result:
                messages.info(request, msg)
            else:
                messages.warning(request, msg)
        except Exception as e:
            msg = _(f'Command raised exception: {str(e)}')
            messages.error(request, msg)

    data = RedisListTableForm(user=request.user).get()
    context = {
        'data': data,
        'form': {
            'body': body,
            'title': _('Block list multiple pop'),
            'buttons': {'save': True, 'cancel': True},
        }
    }

    return render(request, 'Admin/Redis/List/redis_list_blmpop.html', context)
