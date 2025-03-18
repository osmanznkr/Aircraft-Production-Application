from django.db.models import Count, Q
from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from aircrafts import models, serializers, filtersets
from permissions import UserPermission


class InventoryViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """
        ViewSet for managing inventory items with create, retrieve, list, and destroy actions.

        Attributes:
            queryset (QuerySet): The queryset of Inventory objects.
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
            perform_destroy(instance): Prevents deletion of used inventories and inventories that do not belong to the user's team.
    """
    queryset = models.Inventory.objects.all()
    search_fields = ('serial_number',
                     'produced_by__first_name',
                     'produced_by__last_name'
                     )
    ordering_fields = '__all__'
    lookup_field = 'serial_number'
    permission_classes = [UserPermission]
    perm_slug = 'aircrafts.Inventory'
    filterset_class = filtersets.InventoryFilter

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.InventoryCreateSerializer
        if self.action == 'retrieve':
            return serializers.InventoryRetrieveSerializer
        if self.action == 'list':
            return serializers.InventoryListSerializer
        return serializers.InventoryRetrieveSerializer

    # This method was used to control that the user can only produce a inventory associated with their own team.
    def get_queryset(self):
        user_team = self.request.user.profile.team.team
        if user_team == 'ASSEMBLY':
            return super().get_queryset()
        return super().get_queryset().filter(inventory_type=user_team)

    def perform_destroy(self, instance):
        """ Prevent deletion of used inventories and inventories that do not belong to the user's team. """
        user_team = self.request.user.profile.team.team

        # If the user's team does not match the inventory_type, prevent deletion
        if instance.inventory_type != user_team:
            raise PermissionDenied(_('You do not have permission to delete this inventory.'))

        # If the inventory has been used, prevent deletion
        if instance.is_used:
            raise PermissionDenied(_('This inventory has been used and cannot be deleted.'))

        instance.delete()


class InventoryCountViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """
    ViewSet for listing inventory counts, showing how many inventories are in use and how many are not.

    Attributes:
        queryset (QuerySet): The queryset of Inventory objects.
        serializer_class (Serializer): The serializer class for the viewset.
        permission_classes (list): List of permission classes.
        perm_slug (str): Permission slug for the viewset.
        filterset_class (FilterSet): FilterSet class for filtering the queryset.

    Methods:
        list(request, *args, **kwargs): Lists the inventory counts, annotated with used and unused counts.
    """
    queryset = models.Inventory.objects.all()
    serializer_class = serializers.InventoryCountSerializer
    permission_classes = [UserPermission]
    perm_slug = 'aircrafts.Inventory'
    filterset_class = filtersets.InventoryCountFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Annotate the queryset with counts of used and unused Inventories for each aircraft type
        annotated_queryset = queryset.values('inventory_type').annotate(
            total_stock=Count('id'),
            allocated_stock=Count('id', filter=Q(is_used=True)),
            available_stock=Count('id', filter=Q(is_used=False))
        )

        # Paginate the queryset if necessary
        page = self.paginate_queryset(annotated_queryset)
        if page is not None:
            serializer = serializers.InventoryCountSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        # Serialize the queryset and return the response
        serializer = serializers.InventoryCountSerializer(annotated_queryset, many=True)
        return Response(serializer.data)
