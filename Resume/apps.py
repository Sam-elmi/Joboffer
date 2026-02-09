from django.apps import AppConfig


class ResumeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Resume'

    def ready(self):
        from . import signals  # noqa: F401
