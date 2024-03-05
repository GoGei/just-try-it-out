from django import forms
from django.utils.translation import ugettext_lazy as _
from .. import fields, forms as redis_forms
from .serializers.serializers import RedisHashCreateSerializer

PREFIX = 'hash'


class BaseRedisHashForm(redis_forms.BaseRedisForm):
    REDIS_PREFIX = PREFIX


class RedisHashTableForm(BaseRedisHashForm, redis_forms.BaseRedisSearchForm):
    pass


class RedisHashForm(BaseRedisHashForm):
    class Actions(object):
        CREATE = 'create'
        DELETE = 'delete'

    hash_name = fields.KeyWithOptionsField(label=_('Hash name'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.set_options('hash_name')

        actions = self.Actions
        self.serializers_map = {
            actions.CREATE: RedisHashCreateSerializer,
        }
        self.redis_errors = {}

    def _validate(self, data, action):
        serializer = self.serializers_map.get(action, None)
        if not serializer:
            raise ValueError(_(f'Unknown action: {action}'))

        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=False)
        self.redis_errors = serializer.errors

    def validate_create(self, data):
        self._validate(data, self.Actions.CREATE)

    def create(self, data):
        with self.service as r:
            hash_name = self.form_key(data.get('hash_name'))
            items = data.get('items')
            mapping = {item.get('key'): item.get('value') for item in items}
            return r.hset(hash_name, mapping=mapping)

    def delete(self, data):
        hash_name = data.get('hash_name', '')
        if not hash_name:
            return None

        key = data.get('key', '')
        if not key:
            return None

        hash_name = self.form_key(hash_name)
        with self.service as r:
            return r.hdel(hash_name, *[key])

    def get_key(self, key: str):
        if not key:
            return None

        with self.service as r:
            hash_name = self.form_key(key)
            return r.hgetall(hash_name)

    @classmethod
    def response_to_list_of_dicts(cls, response):
        items = []
        if response:
            try:
                items = [
                    {
                        'key': key,
                        'value': value
                    } for key, value in response.items()
                ]
            except Exception:
                pass
        return items


class RedisHashInfoForm(BaseRedisHashForm):
    hash_name = fields.KeyWithOptionsField(label=_('Hash name'))

    def get_key_info(self, key: str):
        key = self.form_key(key)
        with self.service as r:
            full_table = r.hgetall(key)
            keys = r.hkeys(key)
            values = r.hvals(key)
            hlen = r.hlen(key)

            data = {
                'full_table': full_table,
                'keys': keys,
                'values': values,
                'hlen': hlen
            }

        return data


class RedisHashRandFieldsForm(BaseRedisHashForm):
    key = fields.KeyWithOptionsField(with_tags=False)
    count = forms.IntegerField(required=False)
    withvalues = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_options('key')

    def rand_fields(self):
        data = self.cleaned_data
        key = data.get('key')
        count = data.get('count')
        withvalues = data.get('withvalues')

        kwargs = {}
        if count is not None:
            kwargs['count'] = count
        if withvalues is not None:
            kwargs['withvalues'] = withvalues

        with self.service as r:
            key = self.form_key(key)
            return r.hrandfield(key, **kwargs)
