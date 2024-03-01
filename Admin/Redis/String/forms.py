from django import forms
from django.utils.translation import ugettext_lazy as _
from .. import fields, forms as redis_forms


class BaseRedisForm(redis_forms.BaseRedisForm):
    REDIS_PREFIX = 'string'

    def get_data(self, key: str = '*'):
        key = f'{self.base_key}:{key}'
        base_key = f'{self.base_key}:'

        with self.service as r:
            keys = r.keys(key)
            values = r.mget(keys)
            ttls = [r.ttl(key) for key in keys]

            clean_keys = list(map(lambda x: x.replace(base_key, ''), keys))
            return list({'key': key,
                         'value': value,
                         'ttl': None if ttl == -1 else ttl
                         } for key, value, ttl in sorted(zip(clean_keys, values, ttls), key=lambda x: x[0]))


class RedisStringSetForm(BaseRedisForm):
    key = fields.KeyField()
    value = fields.ValueField()
    ex = fields.ExField()
    nx = fields.NxField()
    xx = fields.XxField()

    def clean(self):
        cleaned_data = self.cleaned_data
        nx = cleaned_data.get('nx')
        xx = cleaned_data.get('xx')

        if xx and nx:
            msg = _('NX and XX is not allowed to set together')
            self.add_error('nx', msg)
            self.add_error('xx', msg)

        return cleaned_data

    def set(self):
        data = self.cleaned_data
        keys = ('ex', 'nx', 'xx')

        with self.service as r:
            key = self.form_key(data.get('key'))
            extra = {
                key: value
                for key, value in data.items()
                if value is not None and key in keys
            }
            return r.set(key, data.get('value'), **extra)


class RedisStringTableForm(redis_forms.BaseRedisSearchForm):
    pass


class RedisStringDeleteForm(BaseRedisForm):
    key = fields.KeyWithOptionsField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_options('key')

    def delete(self):
        data = self.cleaned_data
        key = data.get('key')

        with self.service as r:
            return r.delete(f'{self.base_key}:{key}')


class RedisStringCounterForm(BaseRedisForm):
    key = fields.KeyField()
    value = forms.CharField(label=_('Try to path string :)'), required=False)
    int_value = forms.IntegerField(required=False)
    float_value = forms.FloatField(required=False)

    def clean(self):
        data = self.cleaned_data
        value = data.get('value')
        int_value = data.get('int_value')
        float_value = data.get('float_value')

        if not any([value, int_value, float_value]):
            self.add_error(None, _('Please, specify value to increment or decrement'))

        return data

    def execute(self):
        data = self.cleaned_data
        key = data.get('key')
        value = data.get('value')
        int_value = data.get('int_value')
        float_value = data.get('float_value')

        with self.service as r:
            key = f'{self.base_key}:{key}'
            if int_value:
                return r.incrby(key, int_value)
            elif float_value:
                return r.incrbyfloat(key, float_value)
            else:
                for func in (r.incrby, r.incrbyfloat):
                    try:
                        # under redis it is still string that is tried to cast str to int/float
                        return func(key, value)
                    except Exception:
                        pass
            return None


class RedisStringGetDelForm(BaseRedisForm):
    key = fields.KeyWithOptionsField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_options('key')

    def get_del(self):
        with self.service as r:
            key = self.cleaned_data.get('key')
            return r.getdel(self.form_key(key))


class RedisStringGetRangeForm(BaseRedisForm):
    key = fields.KeyWithOptionsField()
    start = forms.IntegerField(label=_('Start'))
    end = forms.IntegerField(label=_('End'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_options('key')

    def get_range(self):
        data = self.cleaned_data
        with self.service as r:
            key = self.form_key(data.get('key'))
            return r.getrange(key, data.get('start'), data.get('end'))


class RedisStringGetSetForm(BaseRedisForm):
    key = fields.KeyField()
    value = fields.ValueField()

    def get_set(self):
        data = self.cleaned_data
        with self.service as r:
            value = self.cleaned_data.get('value')
            return r.getset(self.form_key(data.get('key')), value)


class RedisStringLCSForm(BaseRedisForm):
    key1 = fields.KeyWithOptionsField(label=_('Key-1'))
    key2 = fields.KeyWithOptionsField(label=_('Key-2'))

    with_len = forms.BooleanField(label=_('With length'), required=False)
    with_idx = forms.BooleanField(label=_('With index'), required=False)
    minmatchlen = forms.IntegerField(label=_('With minimum match length'), min_value=1, required=False)
    with_matchlen = forms.BooleanField(label=_('With matches length'), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_options('key1')
        self.set_options('key2')

    def lcs(self):
        data = self.cleaned_data
        with self.service as r:
            kwargs = {
                'key1': f"{self.base_key}:{data.get('key1')}",
                'key2': f"{self.base_key}:{data.get('key2')}",
                'len': data.get('with_len', False),
                'idx': data.get('with_idx', False),
                'minmatchlen': data.get('minmatchlen') or 0,
                'withmatchlen': data.get('with_matchlen', False),
            }
            return r.lcs(**kwargs)
