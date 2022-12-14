import os
import signal
import subprocess
import traceback
import time
import logging
import psutil

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
        self.pid = None
        self.config = configer.ConfigManager().initialize()
        self.LOG = self.config.get('LOG')

    def init_log(self):

        try:
            subprocess.Popen([
                'rm',
                self.LOG,
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except IOError:
            print(traceback.print_exc())
            print(traceback.format_exc())
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
        LOG = self.LOG
        self.init_log()

        try:
            process = self.airodump()  # 启动airodump主进程
        except RuntimeError:
            print(traceback.print_exc())
            print(traceback.format_exc())
            raise RuntimeError

        for count in range(0, 3):
            time.sleep(10)  # 启动等待
            if os.path.exists(LOG) and os.stat(LOG).st_size > 200:
                try:
                    config.set(
                        MAIN_STATUS=True,
                        MAIN_PID=process.pid
                    )
                    return process.pid
                except RuntimeError:
                    print(traceback.print_exc())
                    print(traceback.format_exc())
                    raise RuntimeError
            else:
                print('Airodump start failed')
                self.stop()
                self.init_log()

                raise TimeoutError

        raise SystemError

    def stop(self):
        pid = self.config.get('MAIN_PID')
        if isinstance(pid, str):
            pid = int(pid)
        if pid:
            try:
                if psutil.pid_exists(pid):
                    os.kill(pid, signal.SIGKILL)
                    return True
            except SystemError:
                print(traceback.print_exc())
                print(traceback.format_exc())
                return False
