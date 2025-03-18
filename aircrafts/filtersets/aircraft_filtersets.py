import django_filters

from aircrafts import configs, models


class AircraftFilter(django_filters.FilterSet):
    """
     Filter set for the Inventory model.
    """

    aircraft_type = django_filters.ChoiceFilter(choices=configs.AIRCRAFT_TYPES)

    class Meta:
        model = models.Aircraft
        fields = ('aircraft_type', 'is_active')
