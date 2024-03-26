from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django_hosts import reverse
from core.Utils.Logger.models import ActivityLog
from core.Utils.Logger.enums import LevelChoices
from core.Utils.Logger.services import log_qs_to_list
from core.Utils.Logger.decorators import admin_logger
from core.Utils.Access.decorators import manager_required

from .forms import LoggerFilterForm
from .tables import LoggerTable, LoggerObjectTable


@manager_required
def activity_log_objects_list(request):
    qs = ActivityLog.objects.filter(level=LevelChoices.OBJECT).order_by('-stamp')

    activity_log_filter = LoggerFilterForm(request.GET, queryset=qs)
    qs = activity_log_filter.qs
    data = log_qs_to_list(qs, fields=LoggerObjectTable.Meta.fields)
    table_body = LoggerObjectTable(data)

    table = {
        'body': table_body,
        'filter': {
            'body': activity_log_filter,
            'action': reverse('admin-logger-objects-list', host='admin'),
        },
        'on_empty': {
            'title': _('No logs yet'),
            'description': _('Please, wait for logs')
        }
    }

    return render(request, 'Admin/Logger/activity_log_objects_list.html',
                  {'table': table})


@manager_required
def activity_log_list(request):
    qs = ActivityLog.objects.all().order_by('-stamp')

    activity_log_filter = LoggerFilterForm(request.GET, queryset=qs)
    qs = activity_log_filter.qs
    data = log_qs_to_list(qs, fields=LoggerTable.Meta.fields)
    table_body = LoggerTable(data)

    table = {
        'body': table_body,
        'filter': {
            'body': activity_log_filter,
            'action': reverse('admin-logger-list', host='admin'),
        },
        'on_empty': {
            'title': _('No logs yet'),
            'description': _('Please, wait for logs')
        }
    }

    return render(request, 'Admin/Logger/activity_log_list.html',
                  {'table': table})


@admin_logger
@manager_required
def admin_logger_trigger(request):
    messages.info(request, _('This action has to log the action'))
    return redirect(reverse('admin-logger-list', host='admin'))


@admin_logger(log_on_status=200)
@manager_required
def admin_logger_trigger_with_error(request):
    messages.warning(request, _('This action WILL NOT log the action'))
    return redirect(reverse('admin-logger-list', host='admin'))


@admin_logger
@manager_required
def admin_logger_trigger_params(request, *args, **kwargs):
    messages.info(request, _(f'This action has to log the action with args: {args}, kwargs: {kwargs}'))
    return redirect(reverse('admin-logger-list', host='admin'))
