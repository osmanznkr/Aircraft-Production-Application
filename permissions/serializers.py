from django.contrib.auth.models import Permission
from rest_framework import serializers


class PermissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
