from core.Utils.Logger.models import ActivityLog
from core.Utils.Logger.enums import LevelChoices
from core.Utils.Filters.mongo_fields import MongoDBNullChoiceFilter
from core.Utils.Filters.mongo_filtersets import MongoDBBaseSearchFilterMixin


class LoggerFilterForm(MongoDBBaseSearchFilterMixin):
    level = MongoDBNullChoiceFilter(choices=LevelChoices.choices,
                                    required=False)

    class Meta(MongoDBBaseSearchFilterMixin.Meta):
        model = ActivityLog
        fields = MongoDBBaseSearchFilterMixin.Meta.fields + ('level',)
        search_fields = ('key', 'description', 'user_id', 'obj_id')
