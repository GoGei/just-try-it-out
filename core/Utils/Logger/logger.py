from django.conf import settings
from django.utils import timezone
from django.utils.encoding import force_text
from mongoengine import connection
from .enums import LevelChoices


class Logger(object):
    @staticmethod
    def _get_collection(db, collection=None):
        return db[collection or settings.MONGODB_LOGGER_COLLECTION]

    @staticmethod
    def _get_connection():
        return connection.get_db(alias=settings.MONGODB_LOGGER_ALIAS,
                                 reconnect=False)

    def log(self, level: LevelChoices, key: str, description: str, **kwargs):
        db = self._get_connection()
        collection = self._get_collection(db)
        data = {'stamp': timezone.now(),
                'level': level,
                'key': key,
                'description': force_text(description).format(**kwargs)}
        data.update(**kwargs)
        collection.insert_one(data)

    def debug(self, *args, **kwargs):
        return self.log(LevelChoices.DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        return self.log(LevelChoices.INFO, *args, **kwargs)

    def success(self, *args, **kwargs):
        return self.log(LevelChoices.SUCCESS, *args, **kwargs)

    def warning(self, *args, **kwargs):
        return self.log(LevelChoices.WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        return self.log(LevelChoices.ERROR, *args, **kwargs)

    def critical(self, *args, **kwargs):
        return self.log(LevelChoices.CRITICAL, *args, **kwargs)

    def object(self, key: str, description: str, instance, user, level=LevelChoices.OBJECT, **kwargs):
        class_name = instance.__class__.__name__

        kwargs.update({
            '%s_id' % class_name.lower(): instance.id,
            'user_id': str(user.id)
        })

        return self.log(
            level,
            key,
            description,
            obj_type=class_name,
            obj_id=instance.id,
            **kwargs)


log = Logger()
