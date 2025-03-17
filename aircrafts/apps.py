from django.apps import AppConfig


class AircraftsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aircrafts'

    def ready(self):
        import aircrafts.signals
