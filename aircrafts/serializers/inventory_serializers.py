from typing import Union

from django.core.exceptions import PermissionDenied
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from aircrafts import models, configs


class InventoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an Inventory instance.

    This serializer validates the data to ensure that the user has the necessary permissions
    to create the inventory and sets the user who produced the inventory.

    Meta:
        model (Inventory): The model that this serializer is for.
        fields (list): Fields to include in the serialization.

    Methods:
        validate(data): Validates the input data to ensure the user has permission to create the inventory.
        create(validated_data): Sets the user who produced the inventory and creates the inventory instance.
    """

    class Meta:
        model = models.Inventory
        fields = ['inventory_type', 'aircraft_type']

    # This method was used to control that the user can only produce a inventory associated with their own team.
    def validate(self, data):
        user = self.context['request'].user
        user_team = user.profile.team.team

        if user_team != data['inventory_type']:
            raise PermissionDenied(_('You do not have permission to create this inventory.'))

        return data

    # User who produced the inventory is set as the current user.
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['produced_by'] = user
        return super().create(validated_data)


class InventoryRetrieveSerializer(serializers.ModelSerializer):
    """
        Serializer for retrieving an Inventory instance.

        This serializer provides detailed information about an inventory item, including its type,
        the user who produced it, and the aircraft it is used in (if any).

        Attributes:
            produced_by (StringRelatedField): The user who produced the inventory.
            inventory_type (SerializerMethodField): The type of the inventory.
            aircraft_type (SerializerMethodField): The type of the aircraft the inventory is used in.
            used_in_aircraft (SerializerMethodField): The aircraft the inventory is used in (if any).

        Meta:
            model (Inventory): The model that this serializer is for.
            fields (str): Fields to include in the serialization.

        Methods:
            get_inventory_type(obj): Returns the display name of the inventory type.
            get_aircraft_type(obj): Returns the display name of the aircraft type.
            get_used_in_aircraft(obj): Returns the details of the aircraft the inventory is used in (if any).
        """
    produced_by = serializers.StringRelatedField()
    inventory_type = serializers.SerializerMethodField()
    aircraft_type = serializers.SerializerMethodField()
    used_in_aircraft = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = models.Inventory

    def get_inventory_type(self, obj) -> dict:
        return {
            'type': obj.inventory_type,
            'name': obj.get_inventory_type_display()
        }

    def get_aircraft_type(self, obj) -> dict:
        return {
            'type': obj.aircraft_type,
            'name': obj.get_aircraft_type_display()
        }

    def get_used_in_aircraft(self, obj) -> Union[dict, None]:
        if obj.is_used:
            aircraft = obj.wings.first() or obj.fuselages.first() or obj.tails.first() or obj.avionics.first()
            if aircraft:
                return {
                    'serial_number': aircraft.serial_number,
                    'aircraft_type': aircraft.get_aircraft_type_display(),
                    'assembly_date': aircraft.assembly_date,
                }
        return None


class InventoryListSerializer(serializers.ModelSerializer):
    produced_by = serializers.StringRelatedField()
    inventory_type = serializers.CharField(source='get_inventory_type_display')
    aircraft_type = serializers.CharField(source='get_aircraft_type_display')

    class Meta:
        fields = '__all__'
        model = models.Inventory


class InventoryCountSerializer(serializers.Serializer):
    """
    Serializer for inventory count.

    """
    inventory_type = serializers.SerializerMethodField()
    total_stock = serializers.IntegerField()
    allocated_stock = serializers.IntegerField()
    available_stock = serializers.IntegerField()

    def get_inventory_type(self, obj) -> str:
        return dict(configs.INVENTORY_TYPES)[obj['inventory_type']]
