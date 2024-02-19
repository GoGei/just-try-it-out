from .models import ActivityLog


def log_qs_to_list(qs: ActivityLog.objects, fields: tuple = ('key', 'level', 'stamp', 'description')):
    return [
        {
            key: getattr(item, key) for key in fields
        } for item in qs
    ]
