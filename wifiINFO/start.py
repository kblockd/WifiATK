# -*- coding: utf-8
import time
# from wifiINFO.common import monitor, dataparser, config
from wifiINFO.wifi import WifiATKEngine


def first_start():

    time1 = time.time()

    # config_obj = config.ConfigManager()
    # config_obj.initialize()
    #
    # monitor_obj = monitor.MonitorManager()
    # monitor_obj.start()
    #
    # dataparser_obj = dataparser.Dataparser()
    # dataparser_obj.first_start()
    Engine = WifiATKEngine()

    Engine.start()

    time2 = time.time()
    print('启动成功，消耗时间：{}'.format(time2-time1))


if __name__ == 'wifiINFO.start':
    first_start()
