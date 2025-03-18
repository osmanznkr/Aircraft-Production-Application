from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet

from accounts import serializers, models, configs
from accounts.filtersets import UserFilter
from permissions import UserPermission


class UserRetrieveView(generics.RetrieveAPIView):
    """
    API view to retrieve the authenticated user's details.

    This view returns the details of the currently authenticated user.
    It uses the UserRetrieveSerializer to serialize the user data.

    Methods:
        get_object(): Returns the currently authenticated user.
    """
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserRetrieveSerializer

    def get_object(self):
        """
        Returns the currently authenticated user.
        """
        return self.request.user


class UserViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for retrieving and listing users.

    This ViewSet provides `retrieve` and `list` actions for the User model.
    It uses different serializers for different actions and applies search, ordering, and filtering.

    Attributes:
        queryset (QuerySet): QuerySet of all User objects.
        search_fields (tuple): Fields to search in the User model.
        ordering_fields (str): Fields to order the User model.
        perm_slug (str): Permission slug for the User model.
        permission_classes (list): List of permission classes.
        filterset_class (class): FilterSet class for filtering the User model.
    """
    queryset = get_user_model().objects.all()
    search_fields = ('first_name',
                     'last_name',
                     'email'
                     )
    ordering_fields = '__all__'
    perm_slug = 'accounts.User'
    permission_classes = [UserPermission]
    filterset_class = UserFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.UserRetrieveSerializer
        return serializers.UserListSerializer


class TeamListView(generics.ListAPIView):
    """
    API view to list all teams with the number of members in each team.
    """
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamWithMemberCountSerializer


class TeamTypeListAPIView(generics.ListAPIView):
    """
    API view to list all team types.
    """
    queryset = configs.TEAM_CHOICES
    serializer_class = serializers.TeamTypeSerializer
