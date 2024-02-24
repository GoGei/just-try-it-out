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


class TimeoutField(forms.IntegerField):
    REQUIRED_FOR_BLOCKING_COMMANDS_MSG = _('Timeout is required to blocking commands!')
    TIMEOUT_LIMIT = 30

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _('Timeout'))
        kwargs.setdefault('required', True)
        kwargs.setdefault('min_value', 1)
        kwargs.setdefault('max_value', self.TIMEOUT_LIMIT)
        super().__init__(*args, **kwargs)

    @classmethod
    def clean_timeout(cls, cleaned_data, block: bool = True) -> list:
        block = block if block in (True, False) else cleaned_data.get('block')
        timeout = cleaned_data.get('timeout')

        errors = []
        if block and not timeout:
            errors.append(cls.REQUIRED_FOR_BLOCKING_COMMANDS_MSG)

        return errors
