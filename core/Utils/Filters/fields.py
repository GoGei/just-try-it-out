import django_filters
from django import forms
from django.utils.translation import ugettext as _


class SearchFilterField(django_filters.CharFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _('Search'))
        kwargs.setdefault('method', 'search_qs')
        kwargs.setdefault('widget', self.get_default_widget())
        super().__init__(*args, **kwargs)

    @classmethod
    def get_default_widget(cls):
        return forms.TextInput(attrs={'type': 'search', 'class': 'form-control', 'placeholder': _('Search')})


class IsActiveFilterField(django_filters.BooleanFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _('Is active'))
        kwargs.setdefault('method', 'is_active_filter')
        kwargs.setdefault('widget', self.get_default_widget())
        super().__init__(*args, **kwargs)

    @classmethod
    def get_default_widget(cls):
        choices = [(None, _('Select')), (True, _('Active')), (False, _('Not active'))]
        return forms.Select(attrs={'class': 'form-control'},
                            choices=choices)


class IsFilledFilterForm(django_filters.BooleanFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _('Is filled'))
        kwargs.setdefault('method', 'is_filled_filter')
        kwargs.setdefault('widget', self.get_default_widget())
        super().__init__(*args, **kwargs)

    @classmethod
    def get_default_widget(cls):
        choices = [(None, _('Select')), (True, _('Filled')), (False, _('Not filled'))]
        return forms.Select(attrs={'class': 'form-control'},
                            choices=choices)
