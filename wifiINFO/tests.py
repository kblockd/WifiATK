from django.test import TestCase

import wifiINFO.hostapd
# Create your tests here.
#from .models import *
#from .utils import *
from .views import *
import time


def test_in():
    time1 = time.time()
    LOGNAME = 'meituan-01.csv'
    wifi_lines, station_lines = file_parse(LOGNAME)
    new_station_list = get_station(station_lines)

    count = 0
    for test_station in new_station_list:
        Stationlog.objects.get(bssid=test_station['bssid'],client=test_station['client'])
        count += 1
        if count > 10000:
            break

    time2 = time.time()
    print("耗时：{}".format(time2 - time1))


def test_back():
    import subprocess

    #subprocess.Popen(['top'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p = subprocess.Popen([
    'airodump-ng',
    'wlan0',
    '-w',
    'ABCTEST',
    '--output-format',
    'csv',
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return p




if __name__ == 'wifiINFO.tests':

    # backend_start('meituan')
    #test_in()
    #func_A()
    #func_B()
    # LOGNAME = 'ABCTEST'
    time1 = time.time()
    wifiINFO.hostapd.host('Meituan',6)
    # a = start_airmon(LOGNAME)
    # print(a)
    time2 = time.time()
    print(time2-time1)
