from django.apps import AppConfig


class StudentConfig(AppConfig):
    name = 'student'

    def ready(self):
        from . import signals
