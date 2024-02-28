from django import forms
from django.utils.translation import ugettext_lazy as _
from .. import fields
from ..service import RedisService

PREFIX = 'set'


def clean_key_from_base_key(base_key: str, key: str):
    if not key:
        return key
    key = key.replace(base_key, '')
    if len(key) >= 1:
        key = key[1:]
    return key


def get_options(user, key: str = '*'):
    base_key = RedisService.form_key(user, PREFIX)
    with RedisService() as r:
        key = f'{base_key}:{key}'
        clean_keys = (clean_key_from_base_key(base_key, key) for key in r.keys(key))
        return ((item, item) for item in clean_keys)


class BaseRedisForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.service = RedisService()
        self.redis_prefix = PREFIX
        self.base_key = RedisService.form_key(self.user, self.redis_prefix)
        super().__init__(*args, **kwargs)

    def clean_key(self):
        key = self.cleaned_data.get('key')
        if key:
            key = key.strip()
        return key

    def form_key(self, key: str) -> str:
        return RedisService.form_key(self.user, self.redis_prefix, key)

    def get_data(self, key: str = '*'):
        key = f'{self.base_key}:{key}'
        base_key = f'{self.base_key}:'

        with self.service as r:
            keys = r.keys(key)
            return list({'key': key.replace(base_key, '')} for key in keys)

    def get_sets_on_work(self):
        keys = self.get_keys_on_work()
        with self.service as r:
            sets = [{'key': key,
                     'members': r.smembers(f'{self.base_key}:{key}')} for key in keys]
        return sets

    def get_keys_on_work(self) -> list:
        return [self.cleaned_data.get('key')]


class RedisSetTableForm(BaseRedisForm):
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

    def get(self):
        return self.get_data()


class RedisSetAddForm(BaseRedisForm):
    key = fields.KeyField()
    values = fields.MultipleValuesField()

    def add(self):
        data = self.cleaned_data
        with self.service as r:
            return r.sadd(self.form_key(data.get('key')), *data.get('values'))


class RedisSetCardForm(BaseRedisForm):
    key = fields.KeyField()

    def cardinality(self):
        data = self.cleaned_data
        with self.service as r:
            return r.scard(self.form_key(data.get('key')))


class RedisSetDiffForm(BaseRedisForm):
    main_key = fields.KeyWithOptionsField(label=_('Key to subtract'))
    keys = fields.MultipleValuesField(label=_('Keys'))
    destination = fields.KeyField(label=_('Destination [Set to save result]'), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['main_key'].widget.choices = get_options(self.user)
        self.fields['keys'].widget.choices = get_options(self.user)

    def difference(self):
        data = self.cleaned_data
        destination = data.get('destination')
        keys = [self.form_key(key) for key in data.get('keys')]
        with self.service as r:
            if destination:
                destination = self.form_key(destination)
                return r.sdiffstore(destination, keys)
            return r.sdiff(keys)

    def get_keys_on_work(self) -> list:
        data = self.cleaned_data
        destination = [data.get('destination')] or []
        keys = data.get('keys')
        main_key = [data.get('main_key')]
        return main_key + keys + destination


class RedisSetInterForm(BaseRedisForm):
    keys = fields.MultipleValuesField(label=_('Keys'))
    destination = fields.KeyField(label=_('Destination [Set to save result]'), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keys'].widget.choices = get_options(self.user)

    def intersect(self):
        data = self.cleaned_data
        destination = data.get('destination')
        keys = [self.form_key(key) for key in data.get('keys')]
        with self.service as r:
            if destination:
                destination = self.form_key(destination)
                return r.sinterstore(destination, keys)
            return r.sinter(keys)

    def get_keys_on_work(self) -> list:
        data = self.cleaned_data
        destination = [data.get('destination')] or []
        keys = data.get('keys')
        return keys + destination


class RedisSetMembersForm(BaseRedisForm):
    key = fields.KeyWithOptionsField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['key'].widget.choices = get_options(self.user)

    def members(self):
        data = self.cleaned_data
        key = self.form_key(data.get('key'))
        with self.service as r:
            return r.smembers(key)


class RedisSetInterCardForm(BaseRedisForm):
    keys = fields.MultipleValuesField(label=_('Keys'))
    limit = forms.IntegerField(min_value=1, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keys'].widget.choices = get_options(self.user)

    def intersect_cardinality(self):
        data = self.cleaned_data

        keys = data.get('keys')
        limit = data.get('limit') or 0

        with self.service as r:
            keys = [self.form_key(key) for key in keys]
            return r.sintercard(len(keys), keys, limit)

    def get_keys_on_work(self) -> list:
        data = self.cleaned_data
        keys = data.get('keys')
        return keys


class RedisSetIsMemberForm(BaseRedisForm):
    key = fields.KeyWithOptionsField()
    members = fields.MultipleValuesField(label=_('Members'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['key'].widget.choices = get_options(self.user)

    def ismember(self):
        data = self.cleaned_data

        key = data.get('key')
        members = data.get('members')

        with self.service as r:
            return r.smismember(self.form_key(key), members)


class RedisSetMoveForm(BaseRedisForm):
    source = fields.KeyWithOptionsField(label=_('Source'))
    destination = fields.KeyWithOptionsField(label=_('Destination'))
    member = fields.ValueField(label=_('Member'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].widget.choices = get_options(self.user)
        self.fields['destination'].widget.choices = get_options(self.user)

    def move(self):
        data = self.cleaned_data

        source = self.form_key(data.get('source'))
        destination = self.form_key(data.get('destination'))
        member = data.get('member')

        with self.service as r:
            return r.smove(source, destination, member)

    def get_keys_on_work(self) -> list:
        data = self.cleaned_data
        source = data.get('source')
        destination = data.get('destination')
        return [source, destination]


class RedisSetPopForm(BaseRedisForm):
    key = fields.KeyWithOptionsField()
    count = fields.CountField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['key'].widget.choices = get_options(self.user)

    def pop(self):
        data = self.cleaned_data

        key = self.form_key(data.get('key'))
        count = data.get('count')

        with self.service as r:
            return r.spop(key, count)


class RedisSetRandMemberForm(BaseRedisForm):
    key = fields.KeyWithOptionsField()
    count = fields.CountField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['key'].widget.choices = get_options(self.user)

    def rand_member(self):
        data = self.cleaned_data

        key = self.form_key(data.get('key'))
        count = data.get('count')

        with self.service as r:
            return r.srandmember(key, count)


class RedisSetRemoveForm(BaseRedisForm):
    key = fields.KeyWithOptionsField()
    values = fields.MultipleValuesField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['key'].widget.choices = get_options(self.user)

    def remove(self):
        data = self.cleaned_data

        key = self.form_key(data.get('key'))
        values = data.get('values')

        with self.service as r:
            return r.srem(key, *values)


class RedisSetUnionForm(BaseRedisForm):
    keys = fields.MultipleValuesField(label=_('Keys'))
    destination = fields.KeyField(label=_('Destination [Set to save result]'), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keys'].widget.choices = get_options(self.user)

    def get_keys_on_work(self) -> list:
        data = self.cleaned_data
        destination = [data.get('destination')] or []
        keys = data.get('keys')
        return keys + destination

    def union(self):
        data = self.cleaned_data

        destination = data.get('destination')
        keys = [self.form_key(key) for key in data.get('keys')]

        with self.service as r:
            if destination:
                destination = self.form_key(destination)
                return r.sunionstore(destination, keys)
            return r.sunion(keys)
