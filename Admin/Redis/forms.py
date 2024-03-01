from django import forms
from . import fields
from .service import RedisService
from .utils import clean_key_from_base_key, get_options


class BaseRedisForm(forms.Form):
    REDIS_PREFIX: str = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.service = RedisService()
        self.redis_prefix = self.REDIS_PREFIX
        self.base_key = RedisService.form_key(self.user, self.redis_prefix)
        super().__init__(*args, **kwargs)

    def get_data(self, key: str = '*'):
        key = f'{self.base_key}:{key}'
        base_key = f'{self.base_key}:'

        with self.service as r:
            keys = r.keys(key)
            return list({'key': key.replace(base_key, '')} for key in keys)

    def set_options(self, field: str):
        print(get_options(self.user, prefix=self.redis_prefix))
        self.fields[field].widget.choices = get_options(self.user, prefix=self.redis_prefix)

    def clean_key_from_base_key(self, key: str):
        return clean_key_from_base_key(self.base_key, key)

    def form_key(self, key: str) -> str:
        return self.service.form_key(self.user, self.redis_prefix, key)

    def get(self):
        return self.get_data()


class BaseRedisSearchForm(BaseRedisForm):
    search = fields.SearchValueField()

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
