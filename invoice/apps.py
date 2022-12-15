from django.apps import AppConfig


class InvoiceConfig(AppConfig):
    name = 'invoice'

    def ready(self):
        from . import signals
