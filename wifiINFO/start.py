import time
from wifiINFO.wifi import WifiATKEngine

def first_start():

    time1 = time.time()

    Engine = WifiATKEngine()

    Engine.start()

    time2 = time.time()
    print('启动成功，消耗时间：{}'.format(time2-time1))


if __name__ == 'wifiINFO.start':
    first_start()
