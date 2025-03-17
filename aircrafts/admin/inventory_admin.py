from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from aircrafts import models


@admin.register(models.Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'serial_number', 'inventory_type', 'aircraft_type', 'produced_by', 'production_date', 'is_used')
    list_filter = ('inventory_type', 'aircraft_type', 'produced_by', 'production_date', 'is_used')
    search_fields = ('id', 'serial_number', 'inventory_type', 'aircraft_type', 'produced_by')
    search_help_text = _('''Searchable by id, serial_number, inventory_type, aircraft_type, produced_by fields.''')
