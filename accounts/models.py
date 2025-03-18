import uuid

from auditlog.registry import auditlog
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from accounts import configs
from core.models import BaseModel


class User(AbstractUser):
    """
    Custom User model extending AbstractUse
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, verbose_name=_('First Name'),
                                  help_text=_('First Name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last Name'),
                                 help_text=_('Last Name'))
    email = models.EmailField(_("email address"), blank=True, unique=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def clean_username(self):
        # Clean username by stripping and lowercasing
        self.username = self.username.strip().lower()

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        # Override save method to format first and last names.
        self.first_name = str(self.first_name).strip().title()
        self.last_name = str(self.last_name).strip().upper()
        super(User, self).save(*args, **kwargs)


class Team(BaseModel):
    """
     Team model representing different teams in the organization.
    """
    team = models.CharField(max_length=50, choices=configs.TEAM_CHOICES, verbose_name=_('Team'),
                            help_text=_('Team'), unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'),
                                      help_text=_('Created at'))

    class Meta:
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')

    def __str__(self):
        return self.get_team_display()


class Profile(BaseModel):
    """
    Profile model representing the user's profile.
    """
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='members')

    def clean(self):
        # Validate that a user can only be in one team.
        if Profile.objects.filter(user=self.user).exists() and self.pk is None:
            raise ValidationError(_('A user can only be in one team.'))

    def save(self, *args, **kwargs):
        # Override save method to validate that a user can only be in one team.
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise ValidationError({'detail': str(e)})

    def __str__(self):
        return f"{self.user} - {self.team}"


auditlog.register(User)
