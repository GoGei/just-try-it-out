import django_mongoengine_filter
from django.utils.translation import ugettext as _


class MongoDBNullChoiceFilter(django_mongoengine_filter.ChoiceFilter):
    EMPTY_VALUE = '', _('Select')

    def __init__(self, *args, **kwargs):
        empty_value = kwargs.pop('empty_value', self.EMPTY_VALUE)
        choices = kwargs.pop('choices', [])
        choices = (empty_value,) + tuple(choices)
        kwargs['choices'] = choices
        super().__init__(*args, **kwargs)
