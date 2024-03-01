from .service import RedisService


def clean_key_from_base_key(base_key: str, key: str):
    if not key:
        return key
    key = key.replace(base_key, '')
    if len(key) >= 1:
        key = key[1:]
    return key


def get_options(user, prefix: str, key: str = '*'):
    base_key = RedisService.form_key(user, prefix)
    with RedisService() as r:
        key = f'{base_key}:{key}'
        clean_keys = (clean_key_from_base_key(base_key, key) for key in r.keys(key))
        return list((item, item) for item in clean_keys)
