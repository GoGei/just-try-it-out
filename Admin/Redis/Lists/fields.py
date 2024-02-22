from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class KeyField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _('Key'))
        kwargs.setdefault('max_length', 255)
        super().__init__(*args, **kwargs)


class ValuesField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _('Values'))
        attrs = kwargs.pop('attrs', {})
        attrs.update({
            'class': 'form-control select2',
            'data-select-2-config': {
                'placeholder': _('Enter options'),
                'multiple': 'multiple',
                'tags': 'true',
                'width': '100%',
            }
        })

        kwargs.setdefault('max_length', 1024)
        kwargs.setdefault('widget', forms.SelectMultiple(attrs))

        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return []
        elif not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages['invalid_list'], code='invalid_list')
        return list(map(lambda x: str(x).strip(), value))

    def validate(self, value):
        """Validate that the input is a list or tuple."""
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')
