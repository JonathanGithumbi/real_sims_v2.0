from django.apps import AppConfig


class BillConfig(AppConfig):
    name = 'bill'

    def ready(self):
        from . import signals
