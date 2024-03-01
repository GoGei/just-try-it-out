from django.utils.translation import ugettext_lazy as _
from .. import fields, forms as redis_forms

PREFIX = 'hash'


class BaseRedisHashForm(redis_forms.BaseRedisForm):
    REDIS_PREFIX = PREFIX


class RedisHashTableForm(BaseRedisHashForm, redis_forms.BaseRedisSearchForm):
    pass


class RedisHashForm(BaseRedisHashForm):
    hash_name = fields.KeyWithOptionsField(label=_('Hash name'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_options('hash_name')

    def create(self, data):
        with self.service as r:
            hash_name = self.form_key(data.get('hash_name'))
            items = data.get('items')
            mapping = {item.get('key'): item.get('value') for item in items}
            return r.hset(hash_name, mapping=mapping)

    def delete(self, data):
        hash_name = self.form_key(data.get('hash_name'))
        with self.service as r:
            return r.hdel(hash_name, *[data.get('key')])
