from django import forms
from django.utils.translation import ugettext_lazy as _
from .. import fields, forms as redis_forms

PREFIX = 'sorted-set'


class BaseRedisForm(redis_forms.BaseRedisForm):
    REDIS_PREFIX = PREFIX


class RedisSortedSetTableForm(BaseRedisForm, redis_forms.BaseRedisSearchForm):
    pass


class RedisSortedSetAddForm(BaseRedisForm):
    key = fields.KeyField()
    nx = fields.NxField()
    xx = fields.XxField()
    gt = forms.BooleanField(required=False, label=_(
        '[GT] Only update existing elements if the new score is greater than the current score.'
    ))
    lt = forms.BooleanField(required=False, label=_(
        '[LT] Only update existing elements if the new score is less than the current score.'
    ))
    ch = forms.BooleanField(required=False, label=_(
        '[CH] Modify the return value from the number of new elements added, to the total number of elements changed.'
    ))
    incr = forms.BooleanField(required=False, label=_(
        '[INCR] When this option is specified ZADD acts like ZINCRBY. Only one score-element pair can be specified in this mode.'
    ))

    def add(self, data):
        with self.service as r:
            name = self.form_key(data.pop('key'))
            return r.zadd(name=name, **data)


class RedisSortedSetCardForm(BaseRedisForm):
    key = fields.KeyField()

    def card(self):
        with self.service as r:
            name = self.form_key(self.cleaned_data.get('key'))
            return r.zcard(name)


class RedisSortedSetCountForm(BaseRedisForm):
    key = fields.KeyField()
    min = forms.CharField()
    max = forms.CharField()

    def count(self):
        with self.service as r:
            name = self.form_key(self.cleaned_data.get('key'))
            return r.zcount(name, self.cleaned_data.get('min'), self.cleaned_data.get('max'))


class RedisSortedSetDiffForm(BaseRedisForm):
    keys = fields.KeyWithOptionsField(with_tags=False)
    withscores = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_options('keys')

    def difference(self):
        with self.service as r:
            keys = list(map(self.form_key, self.cleaned_data.get('keys')))
            return r.zdiff(keys, withscores=self.cleaned_data.get('withscores'))


class RedisSortedSetInter(BaseRedisForm):
    class Aggregates(object):
        SUM = 'SUM', _('SUM')
        MIN = 'MIN', _('MIN')
        MAX = 'MAX', _('MAX')

        @property
        def choices(self):
            return [self.SUM, self.MIN, self.MAX]

    keys = fields.KeyWithOptionsField(with_tags=False)
    aggregate = forms.ChoiceField(choices=Aggregates.choices, required=False)
    withscores = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_options('keys')

    def intersect(self):
        with self.service as r:
            keys = list(map(self.form_key, self.cleaned_data.get('keys')))
            return r.zinter(keys,
                            aggregate=self.cleaned_data.get('aggregate') or None,
                            withscores=self.cleaned_data.get('withscores'))


class RedisSortedSetInterCardForm(BaseRedisForm):
    numkeys = forms.IntegerField(min_value=1)
    keys = fields.KeyWithOptionsField(with_tags=False)
    limit = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_options('keys')

    def intersect_cardinality(self):
        with self.service as r:
            keys = list(map(self.form_key, self.cleaned_data.get('keys')))
            return r.zintercard(self.cleaned_data.get('numkeys'), keys, self.cleaned_data.get('limit'))


class RedisSortedSetLexCountForm(BaseRedisForm):
    key = fields.KeyField()
    min = forms.CharField()
    max = forms.CharField()

    def lex_count(self):
        with self.service as r:
            name = self.form_key(self.cleaned_data.get('key'))
            return r.zlexcount(name, self.cleaned_data.get('min'), self.cleaned_data.get('max'))

# TODO POP form
# POPMIN, POPMAX, BPOPMIN, BPOPMAX
# ZMPOP, BZMPOP

# TODO union form
# ZUNION
