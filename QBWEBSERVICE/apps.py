from django.apps import AppConfig


class QbwebserviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'QBWEBSERVICE'

    def ready(self):
        import QBWEBSERVICE.signals
