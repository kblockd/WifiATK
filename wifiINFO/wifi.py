from wifiINFO.common import monitor, attacker
from wifiINFO.common import settings as configer



class WifiATKEngine(object):
    def __init__(self):
        self.config = configer.ConfigManager()
        self.config.initialize()

        self.monitor = monitor.MonitorManager()
        self.attack = None

        self.MAIN_STATUS = False

    def stop(self):
        self.monitor.stop()
        self.attack.stop()
        self.config.on_exit()

    def start(self):
        self.monitor.start()
        self.attack = attacker.AttackManager()

    def start_attack(self):
        self.attack.start()


def cron_data():
    from wifiINFO.common import dataparser

    data = dataparser.Dataparser()
    data.cron_data()
    data.cron_activelog()


def cron_atk():
    from wifiINFO.common import attacker

    attacker.AttackManager().cron_atk()

