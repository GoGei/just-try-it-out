from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class SortedSetItemSerializer(serializers.Serializer):
    score = serializers.FloatField()
    member = serializers.CharField()


class SortedSetCreateSerializer(serializers.Serializer):
    key = serializers.CharField()
    nx = serializers.BooleanField(required=False)
    xx = serializers.BooleanField(required=False)
    gt = serializers.BooleanField(required=False)
    lt = serializers.BooleanField(required=False)
    ch = serializers.BooleanField(required=False)
    incr = serializers.BooleanField(required=False)
    mapping = SortedSetItemSerializer(many=True, required=True, allow_null=False)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        nx = attrs.get('nx')
        xx = attrs.get('xx')
        gt = attrs.get('gt')
        lt = attrs.get('lt')
        incr = attrs.get('incr')
        items = attrs.get('items', [])

        if nx and xx:
            msg = _('NX and XX is not allowed to set together')
            raise serializers.ValidationError({'nx': [msg], 'xx': [msg]})
        if gt and lt:
            msg = _('GT and LT is not allowed to set together')
            raise serializers.ValidationError({'gt': [msg], 'lt': [msg]})
        if incr and len(items) != 1:
            msg = _("Option 'INCR' only works when passing a single element/score pair")
            raise serializers.ValidationError({'incr': [msg]})
        if nx and (gt or lt):
            msg = _("Only one of 'NX', 'LT', or 'GT' may be defined.")
            raise serializers.ValidationError({'nx': [msg], 'gt': [msg], 'lt': [msg]})

        return attrs
