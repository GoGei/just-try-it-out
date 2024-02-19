from django import forms
from django.utils.translation import ugettext_lazy as _
from .service import RedisService


class RedisStringSetForm(forms.Form):
    key = forms.CharField(label=_('Key'), max_length=255)
    value = forms.CharField(label=_('Value'))
    ex = forms.IntegerField(label=_('[EX] Sets an expire flag on seconds.'), min_value=0, required=False)
    nx = forms.BooleanField(label=_('[NX] Set the value only if it does not exist.'), required=False)
    xx = forms.BooleanField(label=_('[XX] Set the value only if it already exists.'), required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.service = RedisService()
        self.base_key = RedisService.form_key(self.user, 'string')
        super().__init__(*args, **kwargs)

    def clean_key(self):
        return self.cleaned_data.get('key').strip()

    def clean_value(self):
        return self.cleaned_data.get('value').strip()

    def clean(self):
        cleaned_data = self.cleaned_data
        nx = cleaned_data.get('nx')
        xx = cleaned_data.get('xx')

        if xx and nx:
            msg = _('NX and XX is not allowed to set together')
            self.add_error('nx', msg)
            self.add_error('xx', msg)

        return cleaned_data

    def get(self):
        key = f'{self.base_key}:*'
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

    def set(self):
        data = self.cleaned_data
        keys = ('ex', 'nx', 'xx')

        with self.service as r:
            key = RedisService.form_key(self.user, 'string', data.get('key'))
            extra = {
                key: value
                for key, value in data.items()
                if value is not None and key in keys
            }
            return r.set(key, data.get('value'), **extra)
