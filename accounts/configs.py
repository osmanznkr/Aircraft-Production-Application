from django.utils.translation import gettext_lazy as _

# Team choices for the Profile model.
TEAM_CHOICES = (
    ('WING', _('Wing Team')),
    ('FUSELAGE', _('Fuselage Team')),
    ('TAIL', _('Tail Team')),
    ('AVIONICS', _('Avionics Team')),
    ('ASSEMBLY', _('Assembly Team'))
)
