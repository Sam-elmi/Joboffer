from django.apps import AppConfig


class JobrequestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'JobRequest'

    def ready(self):
        from . import signals  # noqa: F401
