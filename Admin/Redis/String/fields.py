from django import forms
from django.utils.translation import ugettext_lazy as _


class KeyField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _('Key'))
        kwargs.setdefault('max_length', 255)
        super().__init__(*args, **kwargs)


class ValueField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _('Value'))
        super().__init__(*args, **kwargs)


class ExField(forms.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _('[EX] Sets an expire flag on seconds.'))
        kwargs.setdefault('min_value', 0)
        kwargs.setdefault('required', False)
        super().__init__(*args, **kwargs)


class NxField(forms.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _('[NX] Set the value only if it does not exist.'))
        kwargs.setdefault('required', False)
        super().__init__(*args, **kwargs)


class XxField(forms.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _('[XX] Set the value only if it already exists.'))
        kwargs.setdefault('required', False)
        super().__init__(*args, **kwargs)
