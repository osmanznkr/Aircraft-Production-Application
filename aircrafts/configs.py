from django.utils.translation import gettext_lazy as _

# Tuple of tuples for the aircraft types
AIRCRAFT_TYPES = (
    ('TB2', _('TB-2')),
    ('TB3', _('TB-3')),
    ('AKINCI', _('Akıncı')),
    ('KIZILELMA', _('Kızılelma'))
)

# Tuple of tuples for the inventory types
INVENTORY_TYPES = (
    ('WING', _('Wing')),
    ('FUSELAGE', _('Fuselage')),
    ('TAIL', _('Tail')),
    ('AVIONICS', _('Avionics'))
)
