from rest_framework import serializers


class HashNameField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault('required', True)
        super().__init__(**kwargs)


class KeyField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault('required', True)
        super().__init__(**kwargs)


class ValueField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault('required', True)
        super().__init__(**kwargs)
