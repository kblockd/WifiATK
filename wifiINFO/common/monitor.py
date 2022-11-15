import os
import subprocess
import traceback
import time
import logging

# from wifiINFO.common import config as configer
from wifiINFO.common import settings as configer

logger = logging.getLogger("wifiINFO.monitor")


class MonitorStartError(Exception):
    """ Exception class to raise in case of an invalid interface """

    def __init__(self):
        """
        Construct the class

        param self: A MonitorStartError object
        :type self: MonitorStartError
        :return: None
        :rtype: None
        """

        message = "The monitor process start Failed!"

        Exception.__init__(self, message)


class MonitorManager(object):
    def __init__(self):
        self.process = None
        self.config = configer.ConfigManager()

    def init_log(self):
        config = self.config
        LOG = config.log

        try:
            subprocess.Popen([
                'rm',
                LOG,
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except IOError:
            return False

    def airodump(self):
        config = self.config

        LOGNAME = config.get('LOGNAME')

        MONFACE = config.interfaces['MONFACE']
        MONFACE.set_interface_mode('Monitor')

        try:
            process = subprocess.Popen([
                'airodump-ng',
                MONFACE.name,
                '-w',
                LOGNAME,
                '--output-format',
                'csv',
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return process
        except RuntimeError:
            print(traceback.print_exc())
            print(traceback.format_exc())
            raise RuntimeError

    def start(self):
        config = self.config
        LOG = config.get('LOG')
        self.init_log()

        process = self.airodump()  # 启动airodump主进程
        self.process = process

        for count in range(0, 3):
            time.sleep(10)  # 启动等待
            if os.path.exists(LOG) and os.stat(LOG).st_size > 200:
                config.set(
                    MAIN_STATUS=True
                )
                return process.pid
            else:
                self.stop()
                self.init_log()
                raise TimeoutError

        raise SystemError

    def stop(self):
        process = self.process
        if process is not None:
            process.kill()
