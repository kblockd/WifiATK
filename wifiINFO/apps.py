# -*- coding: utf-8
# import django.apps
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from django.db.models.signals import post_migrate
import os
import sys


def init_data(sender, **kwargs):
    from wifiINFO.models import Conf
    if Conf.objects.count() == 0:
        conf_data = {"id": 1, "MONFACE": None, "ATKFACE": None,
                    "LOGDIR": None, "LOGNAME": None, "LOG":None,
                    "HOST_PID":None, "DNSMASQ_PID":None, "MAIN_STATUS": 0, "ATK_STATUS": 0,
        }
        Conf.objects.create(**conf_data)


class WifiinfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wifiINFO'

    def ready(self):

        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE')

        if run_once is not None:
            return

        os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True'

        post_migrate.connect(init_data, sender=self)

        """规避其他功能执行"""
        if 'runserver' in sys.argv:
            autodiscover_modules('start.py')