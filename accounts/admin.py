from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from accounts import models


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    """
    Admin class for Custom User model.
    """
    list_display = ('id', 'get_full_name', 'email',
                    'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    search_fields = ('id', 'first_name', 'last_name', 'email')
    search_help_text = _('''Searchable by id, first_name, last_name, email fields.''')

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions"
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "usable_password", "password1", "password2"),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        # Define readonly fields based on user permissions
        _required_readonly_fields = ['last_login', 'date_joined']
        # Fields that are readonly for all users
        _readonly_fields = ['is_superuser', 'user_permissions', 'groups', 'is_staff',
                            'password'] + _required_readonly_fields
        # If user is superuser, they can only edit readonly fields
        if request.user.is_superuser:
            return _required_readonly_fields
        elif request.user.has_perm('accounts.reset_password'):
            _readonly_fields.remove('password')
        return _readonly_fields


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Admin class for Team model.
    """
    list_display = ('id', 'team', 'created_at')
    list_filter = ('team', 'created_at')
    search_fields = ('id', 'team', 'members')
    search_help_text = _('''Searchable by id, team, members fields.''')


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin class for Profile model.
    """
    list_display = ('user', 'team')
    list_filter = ('team', 'user')
    search_fields = ('user', 'team')
    search_help_text = _('''Searchable by user, team fields.''')
