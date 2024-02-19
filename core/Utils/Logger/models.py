from django.conf import settings
from django.utils import timezone
from mongoengine import StringField, DateTimeField, DynamicDocument


class Log(object):
    stamp = DateTimeField(required=True, default=timezone.now)
    description = StringField()
    key = StringField(max_length=255, required=False)
    level = StringField(max_length=255, required=False)

    meta = {"db_alias": settings.MONGODB_LOGGER_ALIAS,
            'dynamic': True,
            'allow_inheritance': False,
            'collection': settings.MONGODB_LOGGER_COLLECTION,
            'indexes': ['stamp']
            }

    @property
    def utcstamp(self):
        return timezone.make_aware(self.stamp, timezone.utc)

    @property
    def localstamp(self):
        return timezone.get_current_timezone().normalize(self.utcstamp)

    @property
    def data(self):
        fields = ('key', 'stamp', 'level', 'description', 'id')
        return {field: value for field, value in self._data.items() if field not in fields}


class ActivityLog(Log, DynamicDocument):
    def __str__(self):
        return self.description

    def __repr__(self):
        return self.description
