from django import forms
from django.utils.translation import ugettext_lazy as _
from . import fields
from ..service import RedisService


class BaseRedisForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.service = RedisService()
        self.redis_prefix = 'string'
        self.base_key = RedisService.form_key(self.user, self.redis_prefix)
        super().__init__(*args, **kwargs)

    def clean_key(self):
        search = self.cleaned_data.get('key')
        if search:
            search = search.strip()
        return search

    def clean_value(self):
        search = self.cleaned_data.get('value')
        if search:
            search = search.strip()
        return search

    def clean(self):
        cleaned_data = self.cleaned_data
        nx = cleaned_data.get('nx')
        xx = cleaned_data.get('xx')

        if xx and nx:
            msg = _('NX and XX is not allowed to set together')
            self.add_error('nx', msg)
            self.add_error('xx', msg)

        return cleaned_data

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

    def get(self):
        return self.get_data()


class RedisStringSetForm(BaseRedisForm):
    key = fields.KeyField()
    value = fields.ValueField()
    ex = fields.ExField()
    nx = fields.NxField()
    xx = fields.XxField()

    def set(self):
        data = self.cleaned_data
        keys = ('ex', 'nx', 'xx')

        with self.service as r:
            key = RedisService.form_key(self.user, self.redis_prefix, data.get('key'))
            extra = {
                key: value
                for key, value in data.items()
                if value is not None and key in keys
            }
            return r.set(key, data.get('value'), **extra)


class RedisStringTableForm(BaseRedisForm):
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


class RedisStringDeleteForm(BaseRedisForm):
    key = fields.KeyField()

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

    def clean_value(self):
        return self.cleaned_data.get('value')

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
