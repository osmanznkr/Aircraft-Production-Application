import django_filters

from aircrafts import configs, models


class InventoryFilter(django_filters.FilterSet):
    """
    Filter set for the Inventory model.
    """
    aircraft_type = django_filters.ChoiceFilter(choices=configs.AIRCRAFT_TYPES)
    inventory_type = django_filters.ChoiceFilter(choices=configs.INVENTORY_TYPES)

    class Meta:
        model = models.Inventory
        fields = ('aircraft_type', 'inventory_type', 'is_used')


class InventoryCountFilter(django_filters.FilterSet):
    """
    Filter set for the Inventory model to count the number of inventories produced by each user.
    """
    aircraft_type = django_filters.ChoiceFilter(choices=configs.AIRCRAFT_TYPES)

    class Meta:
        model = models.Inventory
        fields = ('aircraft_type', )
