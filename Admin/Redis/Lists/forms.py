from django import forms
from django.utils.translation import ugettext_lazy as _
from .. import fields, forms as redis_forms

PREFIX = 'list'


class BaseRedisForm(redis_forms.BaseRedisForm):
    REDIS_PREFIX = PREFIX

    def get_data(self, key: str = '*'):
        key = f'{self.base_key}:{key}'
        base_key = f'{self.base_key}:'

        with self.service as r:
            keys = r.keys(key)
            return list({'key': key.replace(base_key, ''),
                         'values': r.lrange(key, 0, -1),
                         'len': r.llen(key),
                         } for key in keys)


class RedisListTableForm(BaseRedisForm, redis_forms.BaseRedisSearchForm):
    pass


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
    values = fields.MultipleValuesField()

    def push(self):
        data = self.cleaned_data

        with self.service as r:
            key = self.form_key(data.get('key'))
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
            key = self.form_key(data.get('key'))
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
            key = self.form_key(data.get('key'))
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

    key = fields.KeyWithOptionsField()
    where = forms.ChoiceField(label=_('Where'), choices=Commands.choices, initial=Commands.BEFORE)
    pivot = forms.CharField(label=_('Pivot'), max_length=2048)
    value = forms.CharField(label=_('Value'), max_length=2048)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_options('key')

    def insert(self):
        data = self.cleaned_data

        with self.service as r:
            key = self.form_key(data.get('key'))
            where = data.get('where')
            pivot = data.get('pivot')
            value = data.get('value')
            return r.linsert(key, where, pivot, value)


class RedisListMoveForm(BaseRedisForm):
    class Commands(object):
        LEFT = 'left', _('Left')
        RIGHT = 'right', _('Right')

        @classmethod
        def choices(cls):
            return [
                cls.LEFT,
                cls.RIGHT,
            ]

    first_list = fields.KeyWithOptionsField(label=_('From'))
    second_list = fields.KeyWithOptionsField(label=_('To'))
    src = forms.ChoiceField(label=_('From first list'), choices=Commands.choices, initial=Commands.LEFT)
    dest = forms.ChoiceField(label=_('To second list'), choices=Commands.choices, initial=Commands.RIGHT)

    block = forms.BooleanField(label=_('Block command'), initial=False, required=False)
    timeout = fields.TimeoutField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_options('first_list')
        self.set_options('second_list')

    def clean_timeout(self):
        errors = fields.TimeoutField.clean_timeout(self.cleaned_data)
        if errors:
            [self.add_error('timeout', error) for error in errors]
        return self.cleaned_data.get('timeout')

    def move(self):
        data = self.cleaned_data
        with self.service as r:
            kwargs = dict(
                first_list=self.form_key(data.get('first_list')),
                second_list=self.form_key(data.get('second_list')),
                src=data.get('src'),
                dest=data.get('dest'),
            )
            if data.get('block') is True:
                return r.blmove(**kwargs, timeout=data.get('timeout'))
            return r.lmove(**kwargs)


class RedisListStructureForm(BaseRedisForm):
    class Commands(object):
        LPUSH = 'lpush'
        RPUSH = 'rpush'
        LPOP = 'lpop'
        RPOP = 'rpop'

    BUTTON_PREFIX = '__'

    key = fields.KeyField()
    values = fields.MultipleValuesField(required=False)
    count = fields.CountField(required=False)

    @classmethod
    def get_first_key_with_prefix(cls, dictionary, prefix: str = BUTTON_PREFIX):
        for key in dictionary:
            if key.startswith(prefix):
                return key
        return None

    def execute(self, command: str):
        data = self.cleaned_data
        command = command.replace(self.BUTTON_PREFIX, '')
        with self.service as r:
            key = self.form_key(data.get('key'))
            count = data.get('count', 1)
            commands = self.Commands

            if command == commands.LPUSH:
                return r.lpush(key, *data.get('values', []))
            if command == commands.RPUSH:
                return r.rpush(key, *data.get('values', []))
            if command == commands.LPOP:
                return r.lpop(key, count)
            if command == commands.RPOP:
                return r.rpop(key, count)
            return None


class RedisListQueueForm(RedisListStructureForm):
    CUSTOM_BUTTONS = [
        {
            'value': _('Push'),
            'name': f'{RedisListStructureForm.BUTTON_PREFIX}{RedisListStructureForm.Commands.LPUSH}',
        },
        {
            'value': _('Pop'),
            'name': f'{RedisListStructureForm.BUTTON_PREFIX}{RedisListStructureForm.Commands.RPOP}',
        },
    ]


class RedisListStackForm(RedisListStructureForm):
    CUSTOM_BUTTONS = [
        {
            'value': _('Push'),
            'name': f'{RedisListStructureForm.BUTTON_PREFIX}{RedisListStructureForm.Commands.LPUSH}',
        },
        {
            'value': _('Pop'),
            'name': f'{RedisListStructureForm.BUTTON_PREFIX}{RedisListStructureForm.Commands.LPOP}',
        },
    ]


class RedisListDequeForm(RedisListStructureForm):
    CUSTOM_BUTTONS = [
        {
            'value': _('Left push'),
            'name': f'{RedisListStructureForm.BUTTON_PREFIX}{RedisListStructureForm.Commands.LPUSH}',
        },
        {
            'value': _('Left pop'),
            'name': f'{RedisListStructureForm.BUTTON_PREFIX}{RedisListStructureForm.Commands.LPOP}',
        },
        {
            'value': _('Right push'),
            'name': f'{RedisListStructureForm.BUTTON_PREFIX}{RedisListStructureForm.Commands.RPUSH}',
        },
        {
            'value': _('Right pop'),
            'name': f'{RedisListStructureForm.BUTTON_PREFIX}{RedisListStructureForm.Commands.RPOP}',
        },
    ]


class RedisListBlockPopForm(BaseRedisForm):
    class Commands(object):
        LPOP = 'lpop'
        RPOP = 'rpop'

    BUTTON_PREFIX = '__'

    CUSTOM_BUTTONS = [
        {
            'value': _('Left pop'),
            'name': f'{BUTTON_PREFIX}{Commands.LPOP}',
        },
        {
            'value': _('Right pop'),
            'name': f'{BUTTON_PREFIX}{Commands.RPOP}',
        },
    ]

    keys = fields.MultipleValuesField(label=_('Keys'))
    timeout = fields.TimeoutField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_options('keys')

    @classmethod
    def get_first_key_with_prefix(cls, dictionary, prefix: str = BUTTON_PREFIX):
        for key in dictionary:
            if key.startswith(prefix):
                return key
        return None

    def clean_timeout(self):
        errors = fields.TimeoutField.clean_timeout(self.cleaned_data, block=False)
        if errors:
            [self.add_error('timeout', error) for error in errors]
        return self.cleaned_data.get('timeout')

    def execute(self, command: str):
        data = self.cleaned_data
        command = command.replace(self.BUTTON_PREFIX, '')

        keys = data.get('keys')
        timeout = data.get('timeout')
        commands = self.Commands
        with self.service as r:
            key_transformer = self.form_key
            if command == commands.LPOP:
                return r.blpop(list(map(lambda x: key_transformer(x), keys)), timeout)
            if command == commands.RPOP:
                return r.brpop(list(map(lambda x: key_transformer(x), keys)), timeout)
            return None


class RedisListBLMPopForm(BaseRedisForm):
    class Commands(object):
        LEFT = 'LEFT', _('Left')
        RIGHT = 'RIGHT', _('Right')

        @classmethod
        def choices(cls):
            return [
                cls.LEFT,
                cls.RIGHT,
            ]

    timeout = fields.TimeoutField(required=True)
    # it has to be exact len as keys
    # numkeys = forms.IntegerField(label=_('Number of keys to POP'), min_value=1)
    keys = fields.MultipleValuesField(label=_('Keys'))
    direction = forms.ChoiceField(label=_('Direction'), choices=Commands.choices, initial=Commands.LEFT)
    count = fields.CountField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_options('keys')

    def clean_timeout(self):
        errors = fields.TimeoutField.clean_timeout(self.cleaned_data, block=True)
        if errors:
            [self.add_error('timeout', error) for error in errors]
        return self.cleaned_data.get('timeout')

    def blmpop(self):
        data = self.cleaned_data

        timeout = data.get('timeout')
        keys = [self.form_key(key) for key in data.get('keys')]
        numkeys = len(keys)
        direction = data.get('direction')
        count = data.get('count')

        with self.service as r:
            return r.blmpop(timeout, numkeys, *keys, direction=direction, count=count)
