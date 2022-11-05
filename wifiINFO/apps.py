import django.apps
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
import os
import sys

class WifiinfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wifiINFO'

    def ready(self):

        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE')

        if run_once is not None:
            return

        if os.path.exists('run.pid'):
            return

        os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True'

        if 'runserver' in sys.argv:
            open('run.pid', 'w+').write(str(os.getpid()))
            autodiscover_modules('start.py')