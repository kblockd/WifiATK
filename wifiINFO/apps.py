# -*- coding: utf-8
# import django.apps
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from django.db.models.signals import post_migrate
import os
import time
import sys


def init_data(sender, **kwargs):
    from wifiINFO.models import Settings
    if Settings.objects.count() == 0:
        conf_list = {"MONFACE": None, "ATKFACE": None, "HOSTFACE": None, "MAIN_PID": None,
                     "LOGDIR": None, "LOGNAME": None, "LOG": None,"ATK_PID": None,
                     "HOST_PID": None, "DNSMASQ_PID": None, "MAIN_STATUS": False, "ATK_STATUS": False,
                     }

        for key in conf_list.keys():
            value = conf_list[key]
            Settings.objects.filter(key=key).update(value=value)


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
        if 'runserver' in sys.argv or 'uwsgi' in sys.argv:
            print('Runserver!')
            time.sleep(10)
            autodiscover_modules('start.py')
