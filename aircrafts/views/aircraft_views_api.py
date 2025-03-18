from rest_framework import mixins, viewsets

from aircrafts import models, serializers
from aircrafts.filtersets import AircraftFilter
from permissions import UserPermission


class AircraftViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    """
    ViewSet for managing aircraft with create, retrieve, list, and update actions.

    Attributes:
        queryset (QuerySet): The queryset of Aircraft objects.
        search_fields (tuple): Fields to search in the queryset.
        ordering_fields (str): Fields to order the queryset.
        lookup_field (str): Field to use for looking up objects.
        permission_classes (list): List of permission classes.
        perm_slug (str): Permission slug for the viewset.
        filterset_class (FilterSet): FilterSet class for filtering the queryset.

    Methods:
        get_serializer_context(): Adds the request to the serializer context.
        get_serializer_class(): Returns the appropriate serializer class based on the action.
        get_queryset(): Returns the queryset based on the user's team.
    """
    queryset = models.Aircraft.objects.all()
    search_fields = ('serial_number',
                     'produced_by__first_name',
                     'produced_by__last_name'
                     )
    ordering_fields = '__all__'
    lookup_field = 'serial_number'
    permission_classes = [UserPermission]
    perm_slug = 'aircrafts.Aircraft'
    filterset_class = AircraftFilter

    def get_serializer_context(self):
        # Add the request to the serializer context for validation and serialization
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.AircraftCreateSerializer
        if self.action == 'retrieve':
            return serializers.AircraftRetrieveSerializer
        if self.action == 'list':
            return serializers.AircraftListSerializer
        if self.action in ['update', 'partial_update']:
            return serializers.AircraftUpdateSerializer
        return serializers.AircraftRetrieveSerializer

    def get_queryset(self):
        # Only allow ASSEMBLY team to view the queryset
        user_team = self.request.user.profile.team.team
        if user_team == 'ASSEMBLY':
            return super().get_queryset()
        return super().get_queryset().none()
