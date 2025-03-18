from rest_framework import generics

from aircrafts import configs, serializers


class InventoryTypeListAPIView(generics.ListAPIView):
    """
    API view to list all inventory types.
    """
    queryset = configs.INVENTORY_TYPES
    serializer_class = serializers.InventoryTypeSerializer
