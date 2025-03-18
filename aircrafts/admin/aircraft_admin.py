from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from aircrafts import models


@admin.register(models.Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    """
    Admin class for Aircraft model.
    """
    list_display = ('id', 'serial_number', 'aircraft_type', 'assembled_by', 'assembly_date')
    list_filter = ('aircraft_type', 'assembled_by', 'assembly_date')
    search_fields = ('id', 'serial_number', 'aircraft_type', 'assembled_by')
    search_help_text = _('''Searchable by id, serial_number, aircraft_type, assembled_by fields.''')
