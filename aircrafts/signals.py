from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from aircrafts import models


@receiver(pre_save, sender=models.Aircraft)
def validate_aircraft(sender, instance, **kwargs):
    # Validate that all related inventory items have the same aircraft_type
    if instance.fuselage.aircraft_type != instance.aircraft_type:
        raise ValidationError(_('Fuselage inventory type must match the aircraft type.'))
    if instance.tail.aircraft_type != instance.aircraft_type:
        raise ValidationError(_('Tail inventory type must match the aircraft type.'))

    # Check if any selected inventory items are already used
    if instance.fuselage.is_used:
        raise ValidationError(_('The selected fuselage has already been used.'))
    if instance.tail.is_used:
        raise ValidationError(_('The selected tail has already been used.'))


@receiver(m2m_changed, sender=models.Aircraft.wings.through)
def validate_wings(sender, instance, action, **kwargs):
    # Validate that the wings being added are not already used and match the aircraft type
    if action == 'pre_add':
        for inventory in kwargs.get('model').objects.filter(pk__in=kwargs.get('pk_set')):
            if inventory.is_used:
                raise ValidationError(_('One of the selected wings has already been used.'))
            if inventory.aircraft_type != instance.aircraft_type:
                raise ValidationError(_('Wing inventory type must match the aircraft type.'))


@receiver(m2m_changed, sender=models.Aircraft.avionics.through)
def validate_avionics(sender, instance, action, **kwargs):
    # Validate that the avionics being added are not already used and match the aircraft type
    if action == 'pre_add':
        for inventory in kwargs.get('model').objects.filter(pk__in=kwargs.get('pk_set')):
            if inventory.is_used:
                raise ValidationError(_('One of the selected avionics has already been used.'))
            if inventory.aircraft_type != instance.aircraft_type:
                raise ValidationError(_('Avionics inventory type must match the aircraft type.'))


@receiver(post_save, sender=models.Aircraft)
def set_inventory_used(sender, instance, **kwargs):
    # Set is_used to True for fuselage and tail after the aircraft is saved
    instance.fuselage.is_used = True
    instance.fuselage.save()
    instance.tail.is_used = True
    instance.tail.save()


@receiver(m2m_changed, sender=models.Aircraft.wings.through)
def set_wings_used(sender, instance, action, **kwargs):
    # Set is_used to True for wings after they are added to the aircraft
    if action == 'post_add':
        for inventory in kwargs.get('model').objects.filter(pk__in=kwargs.get('pk_set')):
            inventory.is_used = True
            inventory.save()


@receiver(m2m_changed, sender=models.Aircraft.avionics.through)
def set_avionics_used(sender, instance, action, **kwargs):
    # Set is_used to True for avionics after they are added to the aircraft
    if action == 'post_add':
        for inventory in kwargs.get('model').objects.filter(pk__in=kwargs.get('pk_set')):
            inventory.is_used = True
            inventory.save()
