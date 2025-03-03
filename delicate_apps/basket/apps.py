from django.apps import AppConfig

class BasketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'delicate_apps.basket'

    #  Import signals
    def ready(self):
        from . import signals 
