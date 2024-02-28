from django_hosts import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from core.Utils.Access.decorators import manager_required
from .forms import (
    RedisHashTableForm, RedisFieldFormSet2
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
