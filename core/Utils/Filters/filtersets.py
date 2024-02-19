import django_filters
from django.db.models import Q
from core.Utils.Filters.fields import (
    IsActiveFilterField, SearchFilterField
)


class BaseFilterMixin(django_filters.FilterSet):
    class Meta:
        fields = ()


class BaseCrmActiveFilterMixin(BaseFilterMixin):
    is_active = IsActiveFilterField()

    def is_active_filter(self, queryset, name, value):
        activity_field = self.Meta.activity_field
        if isinstance(value, bool):
            if activity_field:
                _filter = {activity_field: value}
            else:
                # CrmMixin field
                if value is True:
                    _filter = {'archived_stamp__isnull': True}
                else:
                    _filter = {'archived_stamp__isnull': False}
            queryset = queryset.filter(**_filter)
        return queryset

    class Meta(BaseFilterMixin.Meta):
        fields = BaseFilterMixin.Meta.fields + ('is_active',)
        activity_field = None


class BaseSearchFilterMixin(BaseFilterMixin):
    search = SearchFilterField()

    def search_qs(self, queryset, name, value):
        fields = self.Meta.search_fields
        _filter = Q()
        for field in fields:
            _filter |= Q(**{f'{field}__icontains': value})
        queryset = queryset.filter(_filter)
        return queryset

    class Meta(BaseFilterMixin.Meta):
        fields = BaseFilterMixin.Meta.fields + ('search',)
        search_fields = ()


class BaseFilterForm(BaseCrmActiveFilterMixin, BaseSearchFilterMixin):
    class Meta(BaseCrmActiveFilterMixin.Meta, BaseSearchFilterMixin.Meta):
        fields = BaseCrmActiveFilterMixin.Meta.fields + BaseSearchFilterMixin.Meta.fields
        search_fields = ()
        model = None
