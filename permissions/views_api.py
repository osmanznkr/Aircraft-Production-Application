from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from permissions import serializers


class MyPermissionListView(APIView):
    """
    Lists all authorizations of the requesting user, including group authorizations
    """

    @extend_schema(responses=serializers.PermissionListSerializer(many=True))
    def get(self, request):
        permissions = []
        user_permissions = request.user.user_permissions.all()
        permissions.extend(user_permissions)
        [permissions.extend(group.permissions.all()) for group in request.user.groups.all()]

        serializer = serializers.PermissionListSerializer(permissions, many=True)
        return Response(serializer.data)