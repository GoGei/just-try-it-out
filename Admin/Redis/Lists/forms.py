from django import forms
from django.utils.translation import ugettext_lazy as _
from . import fields
from ..service import RedisService


class BaseRedisForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.service = RedisService()
        self.redis_prefix = 'list'
        self.base_key = RedisService.form_key(self.user, self.redis_prefix)
        super().__init__(*args, **kwargs)

    def clean_key(self):
        search = self.cleaned_data.get('key')
        if search:
            search = search.strip()
        return search

    def get_data(self, key: str = '*'):
        key = f'{self.base_key}:{key}'
        base_key = f'{self.base_key}:'

        with self.service as r:
            keys = r.keys(key)
            return list({'key': key.replace(base_key, ''),
                         'values': r.lrange(key, 0, -1),
                         'len': r.llen(key),
                         } for key in keys)

    def get(self):
        return self.get_data()


class RedisListTableForm(BaseRedisForm):
    search = forms.CharField(label=_('Term to search'), required=False)

    def clean_search(self):
        search = self.cleaned_data.get('search')
        if search:
            search = search.strip()
        return search

    def apply_search(self):
        search = self.cleaned_data.get('search')
        return self.get_data(search)

    def clear(self):
        search = self.cleaned_data.get('search')
        with self.service as r:
            if search:
                names = tuple(map(lambda x: f'{self.base_key}:{x.strip()}', search.split()))
            else:
                names = r.keys(f'{self.base_key}:*')
            return r.delete(*names)


class RedisListPushForm(BaseRedisForm):
    class Commands(object):
        LPUSH = 'lpush', _('LPUSH')
        LPUSH_NX = 'lpush_hx', _('LPUSH [HX]')

        RPUSH = 'rpush', _('RPUSH')
        RPUSH_NX = 'rpush_hx', _('RPUSH [HX]')

        @classmethod
        def choices(cls):
            return [
                cls.LPUSH,
                cls.LPUSH_NX,
                cls.RPUSH,
                cls.RPUSH_NX,
            ]

    key = fields.KeyField()
    command = forms.ChoiceField(label=_('Command'), choices=Commands.choices, initial=Commands.LPUSH)
    values = fields.ValuesField()

    def push(self):
        data = self.cleaned_data

        with self.service as r:
            key = RedisService.form_key(self.user, self.redis_prefix, data.get('key'))
            values = data.get('values')
            command = data.get('command')

            commands = self.Commands
            mapping = {
                commands.LPUSH[0]: r.lpush,
                commands.LPUSH_NX[0]: r.lpushx,

                commands.RPUSH[0]: r.rpush,
                commands.RPUSH_NX[0]: r.rpushx,
            }
            function = mapping.get(command)
            return function(key, *values)


class RedisListTrimForm(BaseRedisForm):
    key = fields.KeyField()
    start = forms.IntegerField(label=_('Start'))
    end = forms.IntegerField(label=_('End'))

    def trim(self):
        data = self.cleaned_data

        with self.service as r:
            key = RedisService.form_key(self.user, self.redis_prefix, data.get('key'))
            return r.ltrim(key, data.get('start'), data.get('end'))


class RedisListSetRemForm(BaseRedisForm):
    class Commands(object):
        SET = 'set', _('Set')
        REM = 'rem', _('Rem')

        @classmethod
        def choices(cls):
            return [
                cls.SET,
                cls.REM,
            ]

    key = fields.KeyField()
    value = forms.CharField(label=_('Value'))
    amount = forms.IntegerField(label=_('Specify index or count'))
    command = forms.ChoiceField(label=_('Command'), choices=Commands.choices, initial=Commands.SET)

    def execute(self):
        data = self.cleaned_data

        with self.service as r:
            key = RedisService.form_key(self.user, self.redis_prefix, data.get('key'))
            value = data.get('value')
            command = data.get('command')
            amount = data.get('amount')

            commands = self.Commands
            mapping = {
                commands.SET[0]: r.lset,
                commands.REM[0]: r.lrem,
            }
            function = mapping.get(command)
            return function(key, amount, value)


class RedisListInsertForm(BaseRedisForm):
    class Commands(object):
        BEFORE = 'before', _('Before')
        AFTER = 'after', _('After')

        @classmethod
        def choices(cls):
            return [
                cls.BEFORE,
                cls.AFTER,
            ]

    key = fields.KeyField()
    where = forms.ChoiceField(label=_('Where'), choices=Commands.choices, initial=Commands.BEFORE)
    pivot = forms.CharField(label=_('Pivot'), max_length=2048)
    value = forms.CharField(label=_('Value'), max_length=2048)

    def insert(self):
        data = self.cleaned_data

        with self.service as r:
            key = RedisService.form_key(self.user, self.redis_prefix, data.get('key'))
            where = data.get('where')
            pivot = data.get('pivot')
            value = data.get('value')
            return r.linsert(key, where, pivot, value)
