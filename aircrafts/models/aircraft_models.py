import datetime
import random

from auditlog.registry import auditlog
from django.contrib.auth import get_user_model
from django.db import models

from aircrafts import configs
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Aircraft(BaseModel):
    """
    Model representing an aircraft.

     Attributes:
        serial_number (str): Serial number of the aircraft.
        aircraft_type (str): Type of the aircraft.
        wings (ManyToManyField): Wings associated with the aircraft.
        fuselage (ForeignKey): Fuselage associated with the aircraft.
        tail (ForeignKey): Tail associated with the aircraft.
        avionics (ManyToManyField): Avionics associated with the aircraft.
        assembled_by (ForeignKey): User who assembled the aircraft.
        assembly_date (DateTimeField): Date when the aircraft was assembled.
        is_active (bool): Indicates if the aircraft is active.

    """
    serial_number = models.CharField(max_length=50, verbose_name=_('Serial Number'),
                                     help_text=_('Serial number of aircraft'), blank=True)
    aircraft_type = models.CharField(max_length=50, choices=configs.AIRCRAFT_TYPES, verbose_name=_('Aircraft Type'),
                                     help_text=_('Aircraft type'))
    wings = models.ManyToManyField('aircrafts.Inventory', related_name='wings',
                                   limit_choices_to={'inventory_type': 'WING'}, verbose_name=_('Wings'),
                                   help_text=_('Wings'))
    fuselage = models.ForeignKey('aircrafts.Inventory', on_delete=models.PROTECT, related_name='fuselages',
                                 limit_choices_to={'inventory_type': 'FUSELAGE'}, verbose_name=_('Fuselage'),
                                 help_text=_('Fuselage'))
    tail = models.ForeignKey('aircrafts.Inventory', on_delete=models.PROTECT, related_name='tails',
                             limit_choices_to={'inventory_type': 'TAIL'}, verbose_name=_('Tail'), help_text=_('Tail'))
    avionics = models.ManyToManyField('aircrafts.Inventory', related_name='avionics',
                                      limit_choices_to={'inventory_type': 'AVIONICS'}, verbose_name=_('Avionics'),
                                      help_text=_('Avionics'))
    assembled_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='assembled_aircrafts',
                                     verbose_name=_('Assembled By'), help_text=_('Assembled by'))
    assembly_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Production Date'),
                                         help_text=_('Production date of aircraft'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'), help_text=_('Is active ?'))

    class Meta:
        verbose_name = _('Aircraft')
        verbose_name_plural = _('Aircrafts')
        ordering = ('-assembly_date',)

    def __str__(self):
        return self.serial_number

    def generate_serial_number(self):
        """
        Generates a unique serial number for the aircraft.
        """
        while True:
            time = datetime.datetime.now()
            year = str(time.year)[2:]
            week = str(time.isocalendar()[1]).zfill(2)
            number = str(random.randint(1000, 9999))
            count = str(Aircraft.objects.all().count()).zfill(4)

            serial_number = f"{self.aircraft_type}-{year}{week}-{number}-{count}"

            if not Aircraft.objects.filter(serial_number=serial_number).exists():
                return serial_number

    def save(self, *args, **kwargs):
        # Generate serial number if not provided
        if not self.serial_number:
            self.serial_number = self.generate_serial_number()
        super().save(*args, **kwargs)


auditlog.register(Aircraft)
