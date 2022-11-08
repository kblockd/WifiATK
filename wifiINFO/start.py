# -*- coding: utf-8
from wifiINFO.wifi import start_airmon, get_interfaces
from wifiINFO.hostapd import init_hostapd
from wifiINFO import config
import os
import time
import traceback


def init_conf():
    LOGNAME = 'TEST123'
    LOGDIR = os.getcwd()
    LOG = "{}/{}-01.csv".format(LOGDIR, LOGNAME)
    try:
        config.set_value('LOGDIR', LOGDIR)
        config.set_value('LOGNAME', LOGNAME)
        config.set_value('LOG', LOG)

        interfaces = get_interfaces()
        MONFACE, ATKFACE = interfaces
        config.set_value('MONFACE', MONFACE)
        config.set_value('ATKFACE', ATKFACE)

        config.set_value('HOST_PID', None)
        config.set_value('DNSMASQ_PID', None)

        config.set_value('MAIN_STATUS', 0)
        config.set_value('ATK_STATUS', 0)
    except:
        print('\n', '>>>' * 20)
        print(traceback.print_exc())
        print('\n', '>>>' * 20)
        print(traceback.format_exc())
        return False


def first_start():

    time1 = time.time()
    init_conf()
    pid = start_airmon()
    init_hostapd()
    time2 = time.time()
    print('启动成功，消耗时间：{}'.format(time2-time1))


if __name__ == 'wifiINFO.start':
    first_start()
    pass
