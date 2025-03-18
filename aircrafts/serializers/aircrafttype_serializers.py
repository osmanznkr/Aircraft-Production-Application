from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class AircraftTypeSerializer(serializers.Serializer):
    """
    Serializer for the aircraft type.
    """
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_type(self, obj) -> str:
        return obj[0]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        return _(obj[1])
