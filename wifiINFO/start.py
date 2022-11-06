# -*- coding: utf-8
from wifiINFO.wifi import start_airmon
from wifiINFO import config
import os
import time

def first_start(LOGNAME):
    config.set_value('LOGDIR', os.getcwd())
    config.set_value('LOGNAME', LOGNAME)

    time1 = time.time()
    pid = start_airmon()
    time2 = time.time()
    print('启动成功，消耗时间：{}'.format(time2-time1))

if __name__ == '__main__':
    pass
    #first_start('TEST123')