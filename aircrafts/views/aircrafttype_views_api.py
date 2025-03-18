from rest_framework import generics

from aircrafts import configs, serializers


class AircraftTypeListAPIView(generics.ListAPIView):
    """
    API view to list all aircraft types.
    """
    queryset = configs.AIRCRAFT_TYPES
    serializer_class = serializers.AircraftTypeSerializer
