from django.apps import AppConfig


class FrontendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.frontend'

    def ready(self):
        from src.frontend import signals