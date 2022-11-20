# -*- coding: utf-8
import datetime

from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from django.db.models.signals import post_migrate
import os
import time
import sys


def init_data(sender, **kwargs):
    from wifiINFO.models import Settings
    if Settings.objects.count() == 0:
        conf_list = {
            "MAIN_STATUS": False,
            "ATK_STATUS": False,
            "LOGDIR": None,
            "LOGNAME": None,
            "LOG": None,
            "MONFACE": None,
            "ATKFACE": None,
            "HOSTFACE": None,
            "MAIN_PID": None,
            "ATK_PID": None,
            "HOST_PID": None,
            "DNSMASQ_PID": None,
            "ATK_BSSID": None,
        }

        create_list = []
        for key in conf_list.keys():
            value = conf_list[key]
            Settings.objects.filter(key=key).update_or_create(key=key, value=value)


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
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('------------------{}:Runserver!------------------'.format(date))
            time.sleep(10)
            autodiscover_modules('start.py')
