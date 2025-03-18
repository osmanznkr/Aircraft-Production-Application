from typing import Union
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from accounts import models


class UserRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for User model retrieve view
    """
    team = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        exclude = (
            'is_active', 'is_staff', 'is_superuser', 'password', 'last_login', 'date_joined', 'groups',
            'user_permissions')

    # Get the team of the user
    def get_team(self, obj) -> Union[dict, None]:
        if hasattr(obj, 'profile') and obj.profile is not None:
            return {
                'type': obj.profile.team.team,
                'name': obj.profile.team.get_team_display()
            }
        return None


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for User model list view
    """
    team = serializers.CharField(source='profile.team.get_team_display', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'team')


class TeamWithMemberCountSerializer(serializers.ModelSerializer):
    """
    Serializer for Team model with member count.
    """
    team = serializers.CharField(source='get_team_display', read_only=True)
    member_count = serializers.IntegerField(source='members.count', read_only=True)

    class Meta:
        model = models.Team
        fields = ('team', 'member_count')


class TeamTypeSerializer(serializers.Serializer):
    """
    Serializer for Team type.
    """
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_type(self, obj) -> str:
        return obj[0]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        return _(obj[1])
