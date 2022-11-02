from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class WifiinfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wifiINFO'

    def ready(self):
        autodiscover_modules('start.py')