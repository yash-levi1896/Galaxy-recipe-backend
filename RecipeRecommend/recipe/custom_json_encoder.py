from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.username  # Serialize the username
        return super().default(obj)

# This is used to serialize QuerySet objects to JSON
def serialize_to_json(queryset):
    return serialize('json', queryset, cls=CustomJSONEncoder)
