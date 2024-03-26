import django_tables2 as tables


class LoggerTable(tables.Table):
    key = tables.Column()
    level = tables.Column()
    stamp = tables.Column()
    description = tables.Column()

    class Meta:
        fields = ('key', 'level', 'stamp', 'description')
        template_name = "django_tables2/bootstrap4.html"


class LoggerObjectTable(LoggerTable):
    data = tables.JSONColumn()

    class Meta(LoggerTable.Meta):
        fields = LoggerTable.Meta.fields + ('data',)
