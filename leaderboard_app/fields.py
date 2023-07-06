from django.core.exceptions import ValidationError
from django.db import models

class FloatListField(models.Field):
    description = "A list of floats represented as a comma-separated string"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        if value == '':
            return []

        return [float(x) for x in value.split(',')]

    def to_python(self, value):
        if isinstance(value, list):
            return value

        if value is None:
            return value

        try:
            return [float(x) for x in value.split(',')]
        except Exception as e:
            raise ValidationError(f"Invalid float list: {e}")

    def get_prep_value(self, value):
        if value is None:
            return value

        return ','.join(str(x) for x in value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def get_internal_type(self):
        return "TextField"
