from django.core.exceptions import PermissionDenied
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from aircrafts import models, configs


class InventoryCreateSerializer(serializers.ModelSerializer):
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

    def get_used_in_aircraft(self, obj) -> dict | None:
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
    inventory_type = serializers.SerializerMethodField()
    total_stock = serializers.IntegerField()
    allocated_stock = serializers.IntegerField()
    available_stock = serializers.IntegerField()


    def get_inventory_type(self, obj) -> str:
        return dict(configs.INVENTORY_TYPES)[obj['inventory_type']]