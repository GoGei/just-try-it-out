from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class LevelChoices(TextChoices):
    DEBUG = 'DEBUG', _('Debug')
    INFO = 'INFO', _('Info')
    SUCCESS = 'SUCCESS', _('Success')
    WARNING = 'WARNING', _('Warning')
    ERROR = 'ERROR', _('Error')
    CRITICAL = 'CRITICAL', _('Critical')
    OBJECT = 'OBJECT', _('Object')
