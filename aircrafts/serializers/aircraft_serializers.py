from django.core.exceptions import ValidationError, PermissionDenied
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from aircrafts import models


class AircraftCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an Aircraft instance.

    This serializer validates the data to ensure that the user has the necessary permissions
    and that the selected inventory items (fuselage, tail, wings, and avionics) match the aircraft type
    and have not been used before.

    Meta:
        model (Aircraft): The model that this serializer is for.
        exclude (tuple): Fields to exclude from the serialization.

    Methods:
        validate(data): Validates the input data to ensure it meets the necessary conditions.
    """
    class Meta:
        model = models.Aircraft
        exclude = ('assembled_by', 'assembly_date', 'serial_number')

    def validate(self, data):
        # Check if the user has permission to assembly an airplane
        user = self.context['request'].user
        user_team = user.profile.team.team

        # Only ASSEMBLY team can assembly an airplane
        if user_team != 'ASSEMBLY':
            raise PermissionDenied(_('You do not have permission to assembly an airplane.'))

        # Validate fuselage and tail
        if data['fuselage'].aircraft_type != data['aircraft_type']:
            raise ValidationError(_('Fuselage inventory type must match the aircraft type.'))
        if data['tail'].aircraft_type != data['aircraft_type']:
            raise ValidationError(_('Tail inventory type must match the aircraft type.'))
        if data['fuselage'].is_used:
            raise ValidationError(_('The selected fuselage has already been used.'))
        if data['tail'].is_used:
            raise ValidationError(_('The selected tail has already been used.'))

        # Validate wings
        wings = data.get('wings', [])
        # An aircraft must have exactly 2 wings
        if len(wings) != 2:
            raise ValidationError(_('An aircraft must have exactly 2 wings.'))
        for wing in wings:
            if wing.is_used:
                raise ValidationError(_('One of the selected wings has already been used.'))
            if wing.aircraft_type != data['aircraft_type']:
                raise ValidationError(_('Wing inventory type must match the aircraft type.'))

        # Validate avionics
        for avionic in data.get('avionics', []):
            if avionic.is_used:
                raise ValidationError(_('One of the selected avionics has already been used.'))
            if avionic.aircraft_type != data['aircraft_type']:
                raise ValidationError(_('Avionics inventory type must match the aircraft type.'))

        return data

    # User who produced the aircraft is set as the current user.
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['assembled_by'] = user
        return super().create(validated_data)


class AircraftRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving an Aircraft instance.

    This serializer provides detailed information about an aircraft, including its type,
    the user who assembled it, and the associated inventory items (fuselage, tail, wings, and avionics).

    Attributes:
        aircraft_type (SerializerMethodField): The type of the aircraft.
        assembled_by (StringRelatedField): The user who assembled the aircraft.
        fuselage (SerializerMethodField): The fuselage of the aircraft.
        tail (SerializerMethodField): The tail of the aircraft.
        wings (SerializerMethodField): The wings of the aircraft.
        avionics (SerializerMethodField): The avionics of the aircraft.

    Meta:
        model (Aircraft): The model that this serializer is for.
        fields (str): Fields to include in the serialization.

    Methods:
        get_aircraft_type(obj): Returns the display name of the aircraft type.
        get_tail(obj): Returns the details of the tail of the aircraft.
        get_fuselage(obj): Returns the details of the fuselage of the aircraft.
        get_wings(obj): Returns the details of the wings of the aircraft.
        get_avionics(obj): Returns the details of the avionics of the aircraft.
    """
    aircraft_type = serializers.SerializerMethodField()
    assembled_by = serializers.StringRelatedField()
    fuselage = serializers.SerializerMethodField()
    tail = serializers.SerializerMethodField()
    wings = serializers.SerializerMethodField()
    avionics = serializers.SerializerMethodField()

    class Meta:
        model = models.Aircraft
        fields = '__all__'

    # Get the aircraft type of the aircraft
    def get_aircraft_type(self, obj) -> dict:
        return obj.get_aircraft_type_display()

    # Get the tail of the aircraft
    def get_tail(self, obj) -> dict:
        return {
            'serial_number': obj.tail.serial_number,
            'produced_by': obj.tail.produced_by.get_full_name(),
            'production_date': obj.tail.production_date,
        }

    # Get the fuselage of the aircraft
    def get_fuselage(self, obj) -> dict:
        return {
            'serial_number': obj.fuselage.serial_number,
            'produced_by': obj.fuselage.produced_by.get_full_name(),
            'production_date': obj.fuselage.production_date,
        }

    # Get the wings of the aircraft
    def get_wings(self, obj) -> list:
        return [
            {
                'serial_number': wing.serial_number,
                'produced_by': wing.produced_by.get_full_name(),
                'production_date': wing.production_date,
            }
            for wing in obj.wings.all()
        ]

    # Get the avionics of the aircraft
    def get_avionics(self, obj) -> list:
        return [
            {
                'serial_number': avionic.serial_number,
                'produced_by': avionic.produced_by.get_full_name(),
                'production_date': avionic.production_date,
            }
            for avionic in obj.avionics.all()
        ]


class AircraftListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Aircraft instances.
    """
    aircraft_type = serializers.CharField(source='get_aircraft_type_display')
    assembled_by = serializers.StringRelatedField()

    class Meta:
        model = models.Aircraft
        fields = ('id', 'serial_number', 'aircraft_type', 'assembled_by', 'assembly_date')


class AircraftUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an Aircraft instance.
    """
    class Meta:
        model = models.Aircraft
        fields = ('is_active',)
