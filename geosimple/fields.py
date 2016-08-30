from django.db import models
from django.db.models.fields.subclassing import Creator

from geosimple.utils import Geohash, convert_to_point


class GeohashField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 12
        kwargs['db_index'] = True
        super(GeohashField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return None
        if isinstance(value, str):
            return Geohash(value)
        return convert_to_point(value).geohash

    def contribute_to_class(self, cls, name, virtual_only=False):
        setattr(cls, name, Creator(self))
        super(GeohashField, self).contribute_to_class(cls, name, virtual_only=virtual_only)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^geosimple\.fields\.GeohashField"])
except:
    pass
