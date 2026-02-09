from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Account'

    def ready(self):
        from . import signals  # noqa: F401
