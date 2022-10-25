import time,datetime
import signal,subprocess
from django.shortcuts import render

from time import sleep
from wifiINFO.utils import *
from wifiINFO.models import *


@myasync
def func_A():
    print("字符串1")
    sleep(5)
    print("字符串2")

def func_B():
    print("字符串3")


#获取mon接口
def get_interface():
    '''Returns List of AirmonIface objects known by airmon-ng'''
    p = run_cmd(['airmon-ng'])

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

    return interface


#Wi-Fi表格式
def get_wifi(wifi_lines):
    Wifis = []
    for line in wifi_lines:

        try:
            data_list = line.split(',')

            if len(data_list) < 15:
                continue

            Wifi = {}
            Wifi['bssid'] = data_list[0].strip()
            Wifi['essid'] = is_null(data_list[13].strip())
            Wifi['channel'] = data_list[4].strip()
            Wifi['privacy'] = is_null(data_list[5].strip())
            Wifi['cipher'] = is_null(data_list[6].strip())
            Wifi['authentication'] = is_null(data_list[7].strip())

            Wifis.append(Wifi)

        except Exception as e:
            print(e)

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
            Station['bssid'] = data_list[5][0:17].strip() if validate_mac(data_list[5][0:17].strip()) else None
            Station['essid'] = is_null(data_list[5][18:].strip())
            Stations.append(Station)

        except Exception as e:
            print(e)

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

            temp_value.essid = new_wifi['essid'],
            temp_value.channel = new_wifi['channel'],
            temp_value.privacy = new_wifi['privacy'],
            temp_value.cipher = new_wifi['cipher'],
            temp_value.authentication = new_wifi['authentication'],
            temp_value.last_time = datetime.datetime.now()

            update_list.append(temp_value)

    Wifilog.objects.bulk_create(create_list)
    Wifilog.objects.bulk_update(
        update_list, ['essid', 'channel', 'privacy', 'cipher', 'authentication']
    )


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

    Stationlog.objects.bulk_create(create_list)
    Stationlog.objects.bulk_update(
        update_list, ['essid', 'last_time']
    )


def backend_start(LOGNAME):
 #   remove_files(LOGNAME)
    LOG = LOGNAME+'-01.csv'
    start_airmon(LOG)

    count = 0
    while True:
        sleep(60)
        time1 = time.time()
        wifi_lines, station_lines = file_parse(LOG)
        data_wifi(wifi_lines)
        data_station(station_lines)
        count += 1
        print(count)
        time2 = time.time()
        print('消耗:{}'.format(time2-time1))


#启动
def start_airmon(LOGNAME):
    LOG = LOGNAME+'-01.csv'
    try:
        os.system('rm '+LOG)
        interface = get_interface()

        process = subprocess.Popen([
            'airodump-ng',
            interface,
            '-w',
            LOGNAME,
            '--output-format',
            'csv',
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(e)
        return False

    for count in range(0,10):  # 启动
        sleep(3)  # 启动等待

        if LOG in os.listdir('.'):
            if os.stat(LOG).st_size > 300:
               # os.kill(process.pid, signal.SIGKILL)   测试用
                return process.pid

    try:
        os.kill(process.pid, signal.SIGKILL)
        return False
    except:
        return False


#Deauth
def deauth(interface, bssid):
    try:
        p = run_cmd([
            "mdk4",
            interface,
            "d",
            "-s",
            "20",
            "-c",
            "6",
            "-B",
            bssid
        ])
    except Exception as e:
        print(e)


