from rest_framework import serializers
from . import fields


class RedisHashItemSerializer(serializers.Serializer):
    key = fields.KeyField()
    value = fields.ValueField()


class RedisHashCreateSerializer(serializers.Serializer):
    hash_name = fields.HashNameField()
    items = RedisHashItemSerializer(many=True, required=True, allow_null=False)
