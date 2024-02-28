from .. import fields, forms as redis_forms

PREFIX = 'hash'


class BaseRedisForm(redis_forms.BaseRedisForm):
    REDIS_PREFIX = PREFIX


class RedisHashTableForm(redis_forms.BaseRedisSearchForm):
    pass
