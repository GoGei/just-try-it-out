from redis import Redis
from django.conf import settings
from core.User.models import User


class RedisService(object):
    def __init__(self):
        self.settings = {
            'host': settings.REDIS_HOST,
            'port': settings.REDIS_PORT,
            'db': settings.REDIS_DB,
        }

    def __enter__(self) -> Redis:
        self.redis = Redis(**self.settings, charset="utf-8", decode_responses=True)
        return self.redis

    def __exit__(self, *args, **kwargs):
        pass

    @classmethod
    def form_key(cls, user: User, *args) -> str:
        extra = ':'.join(list(map(str, args)))
        return f'admin:redis:{str(user.id)}:{extra}'
