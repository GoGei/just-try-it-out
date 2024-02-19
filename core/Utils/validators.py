from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator

PhoneValidator = RegexValidator(
    regex=r'"^\\+?[1-9][0-9]{7,14}$"',
    message=_("Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed'.")
)


class ContainsUpperCaseValidator(object):
    def __call__(self, value):
        if not any(e.isupper() for e in value):
            raise ValidationError(_('Has to contain at least one upper case letter'))
        return value


class ContainsLowerCaseValidator(object):
    def __call__(self, value):
        if not any(e.islower() for e in value):
            raise ValidationError(_('Has to contain at least one lower case letter'))
        return value


class ContainsSpecialCharValidator(object):
    def __init__(self, special_chars='!@#$%^&*()-+?_=,<>/'):
        self.special_chars = special_chars

    def __call__(self, value):
        if not any(e in self.special_chars for e in value):
            raise ValidationError(_('Has to contain at least one special character: "%s"' % self.special_chars))
        return value


PasswordValidators = (
    MaxLengthValidator(limit_value=36),
    MinLengthValidator(limit_value=8),
    ContainsUpperCaseValidator(),
    ContainsLowerCaseValidator(),
    ContainsSpecialCharValidator(special_chars='!@#.'),
)
