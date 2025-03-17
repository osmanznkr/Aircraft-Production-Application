import datetime
import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from aircrafts import configs
from core.models import BaseModel


class Inventory(BaseModel):
    """
    Model representing an inventory used in aircraft production.

    Attributes:
        serial_number (str): Unique serial number of the inventory.
        inventory_type (str): Type of the inventory (e.g., Wing, Fuselage).
        aircraft_type (str): Type of the aircraft the inventory is used in (e.g., TB2, AKINCI).
        produced_by (User): User who produced the inventory.
        production_date (datetime): Date and time when the inventory was produced.
        is_used (bool): Indicates whether the inventory has been used in an aircraft.
    """
    serial_number = models.CharField(max_length=50, verbose_name=_('Serial Number'),
                                     help_text=_('Serial number of inventory'), unique=True, blank=True)
    inventory_type = models.CharField(max_length=50, choices=configs.INVENTORY_TYPES, verbose_name=_('Inventory Type'),
                                 help_text=_('Inventory type'))
    aircraft_type = models.CharField(max_length=50, choices=configs.AIRCRAFT_TYPES, verbose_name=_('Aircraft Type'),
                                     help_text=_('Aircraft type'))
    produced_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='produced_inventories',
                                    verbose_name=_('Produced By'), help_text=_('Produced by'))
    production_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Production Date'),
                                           help_text=_('Production date of inventory'))
    is_used = models.BooleanField(default=False, verbose_name=_('Is Used'),
                                  help_text=_('Was inventory used in an aircraft?'))

    class Meta:
        verbose_name = _('Inventory')
        verbose_name_plural = _('Inventories')
        ordering = ('-production_date',)

    def __str__(self):
        return self.serial_number

    def generate_serial_number(self):
        """
        Generates a unique serial number for the inventory.
        """
        while True:
            time = datetime.datetime.now()
            year = str(time.year)[2:]
            week = str(time.isocalendar()[1]).zfill(2)
            number = str(random.randint(1000, 9999))
            count = str(Inventory.objects.all().count()).zfill(4)

            serial_number = f"{self.aircraft_type}-{self.inventory_type}-{year}{week}-{number}-{count}"

            if not Inventory.objects.filter(serial_number=serial_number).exists():
                return serial_number

    def clean(self):
        # Check if the user is trying to create a inventory that does not belong to their team
        user_team = self.produced_by.profile.team.team

        # İf the user is not in the team that the inventory belongs to, raise a validation error
        if user_team != self.inventory_type:
            raise ValidationError(_('You do not have permission to create this inventory.'))

    def save(self, *args, **kwargs):
        self.clean()
        if not self.serial_number:
            self.serial_number = self.generate_serial_number()
        super(Inventory, self).save(*args, **kwargs)
