from django.apps import AppConfig


class TruckserviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'truckService'
    def ready(self):
        import truckService.signals