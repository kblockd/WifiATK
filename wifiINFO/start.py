import time
from wifiINFO.wifi import WifiATKEngine


def first_start():

    Engine = WifiATKEngine()

    Engine.start()



if __name__ == 'wifiINFO.start':
    first_start()
