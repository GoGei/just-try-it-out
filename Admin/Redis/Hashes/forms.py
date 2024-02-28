from django import forms
from django.utils.translation import ugettext_lazy as _
from .. import fields
from ..service import RedisService
from ..utils import get_options as get_options_base

PREFIX = 'hash'


def get_options(user, key: str = '*'):
    return get_options_base(user, PREFIX, key)


class BaseRedisForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.service = RedisService()
        self.redis_prefix = PREFIX
        self.base_key = RedisService.form_key(self.user, self.redis_prefix)
        super().__init__(*args, **kwargs)

    def form_key(self, key: str) -> str:
        return RedisService.form_key(self.user, self.redis_prefix, key)

    def get_data(self, key: str = '*'):
        key = f'{self.base_key}:{key}'
        base_key = f'{self.base_key}:'

        with self.service as r:
            keys = r.keys(key)
            return list({'key': key.replace(base_key, '')} for key in keys)

    # def get_sets_on_work(self):
    #     keys = self.get_keys_on_work()
    #     with self.service as r:
    #         sets = [{'key': key,
    #                  'members': r.smembers(f'{self.base_key}:{key}')} for key in keys]
    #     return sets
    #
    # def get_keys_on_work(self) -> list:
    #     return [self.cleaned_data.get('key')]


class RedisHashTableForm(BaseRedisForm):
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

    def get(self):
        return self.get_data()


from django.forms import formset_factory


class RedisFieldForm(forms.Form):
    field = forms.CharField(max_length=100)
    value = forms.CharField(max_length=100)


RedisFieldFormSet = formset_factory(RedisFieldForm, extra=10)


class RedisFieldFormSet2(RedisFieldFormSet):
    def save(self):
        print(self.cleaned_data)
