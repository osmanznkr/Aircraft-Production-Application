import django_filters
from django.contrib.auth import get_user_model

from accounts import configs


class UserFilter(django_filters.FilterSet):
    """
        Filter set for the User model.
    """
    team = django_filters.ChoiceFilter(choices=configs.TEAM_CHOICES, field_name='profile__team__team')

    class Meta:
        model = get_user_model()
        fields = ['email', 'team']
