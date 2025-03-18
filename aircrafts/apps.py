from django.apps import AppConfig


class AircraftsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aircrafts'

    # This method is called when the app is ready to be used.
    def ready(self):
        import aircrafts.signals
