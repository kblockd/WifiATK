import re
import logging
import traceback
import datetime
import linecache

from wifiINFO.common import utils
# from wifiINFO.common import config as configer
from wifiINFO.common import settings as configer

from wifiINFO.models import Wifilog, Stationlog, Activelog

logger = logging.getLogger("wifiINFO.dataparser")


class Dataparser(object):
    def __init__(self):
        self.config = configer.ConfigManager().initialize()
        if not self.config.get('MAIN_STATUS'):
            print('NO_MAIN_STATUS')
            raise False

        try:
            self._wifi_data, self._station_data = self.file_parse()
        except IOError:
            self.config.on_exit()
            raise IOError

    def first_start(self):
        wifi_data = self._wifi_data
        station_data = self._station_data
        
        self.data_wifi(wifi_data)
        self.data_station(station_data)

    def file_parse(self):  # 文件解析
        inputfile = self.config.log  # 输入源文件

        try:
            fp = open(inputfile, 'r')
        except IOError:
            raise IOError

        keyword = 'Station'  # 切分的关键字
        key_line = None
        count = 1

        for each_line in fp:
            m = re.search(keyword, each_line)  # 查询关键字
            if m is not None:
                key_line = count  # 将关键字的行号
            count += 1

        if key_line is None:
            raise KeyError

        lines = count + 1  # 文件总行数

        wifi_lines = linecache.getlines(inputfile)[2:key_line - 1]
        station_lines = linecache.getlines(inputfile)[key_line:lines]
        fp.close()

        return wifi_lines, station_lines

    @staticmethod
    def get_wifi(wifi_data):  # Wifi格式化
        Wifis = list()
        for line in wifi_data:

            try:
                data_list = line.split(',')

                if len(data_list) < 15:
                    continue

                Wifi = dict()
                Wifi['bssid'] = data_list[0].strip() if utils.is_mac_validate(data_list[0].strip()) else None
                Wifi['essid'] = utils.is_data_null(data_list[13].strip())
                Wifi['channel'] = data_list[3].strip()
                if not str(Wifi['channel']).isdigit():
                    Wifi['channel'] = '-1'
                Wifi['privacy'] = utils.is_data_null(data_list[5].strip())
                Wifi['cipher'] = utils.is_data_null(data_list[6].strip())
                Wifi['authentication'] = utils.is_data_null(data_list[7].strip())

                Wifis.append(Wifi)

            except Exception as e:
                print(e)
                print('\n', '>>>' * 20)
                print(traceback.print_exc())
                print('\n', '>>>' * 20)
                print(traceback.format_exc())

        return Wifis

    @staticmethod
    def get_station(station_data):   # Station格式化
        Stations = list()

        for line in station_data:
            try:
                data_list = line.split(', ')

                if len(data_list) != 6:
                    continue

                Station = dict()
                Station['client'] = data_list[0].strip()
                Station['client'] = data_list[0].strip() if utils.is_mac_validate(data_list[0].strip()) else None
                Station['bssid'] = data_list[5][0:17].strip() if utils.is_mac_validate(data_list[5][0:17].strip()) \
                    else None
                Station['essid'] = utils.is_data_null(data_list[5][18:].strip())
                Stations.append(Station)

            except Exception as e:
                print(e)
                print('\n', '>>>' * 20)
                print(traceback.print_exc())
                print('\n', '>>>' * 20)
                print(traceback.format_exc())

        return Stations

    def data_wifi(self, wifi_data):
        """
        添加与修改分流
            @if
                完全相同则跳过
            @elif
                bssid不存在，新增
            @else
                bssid存在,任意变换则更新
        """
        new_wifi_list = self.get_wifi(wifi_data)

        old_wifi_query = Wifilog.objects.all()

        old_wifi_set = set(
            old_wifi_query.values_list('bssid', 'essid', 'channel', 'privacy', 'cipher', 'authentication'))
        old_bssid_set = set(old_wifi_query.values_list('bssid'))
        create_list = []
        update_list = []

        for new_wifi in new_wifi_list:
            if tuple(new_wifi.values()) in old_wifi_set:
                continue
            elif tuple({'bssid': new_wifi['bssid']}.values()) not in old_bssid_set:
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
        except ValueError:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())

    def data_station(self, station_data):
        """
        添加与修改分流
            @if
                完全相同则跳过
            @elif
                client+bssid不存在，新增
            @else
                client与bssid存在，essid不存在，更新essid列表
        """

        new_station_list = self.get_station(station_data)  # 解析station类目文本

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
        except ValueError:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())

    def cron_activelog(self):
        config = self.config
        if not config.get('MAIN_STATUS'):
            return

        wifi_data = self._wifi_data
        station_data = self._station_data
        
        new_wifi_list = self.get_wifi(wifi_data)
        new_station_list = self.get_station(station_data)

        create_list = []

        ATK_BSSID = config.get('ATK_BSSID')

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

            client = utils.is_data_null(','.join(client))
            essid = utils.is_data_null(essid)

            if bssid == ATK_BSSID:
                ATK_STATUS = True
            else:
                ATK_STATUS = False

            create_list.append(
                Activelog(
                    bssid=bssid,
                    essid=essid,
                    client=client,
                    channel=channel,
                    privacy=privacy,
                    cipher=cipher,
                    authentication=authentication,
                    ATK_STATUS=ATK_STATUS
                )
            )

        try:
            Activelog.truncate()
            Activelog.objects.bulk_create(create_list)

        except ValueError:

            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())

            pass

    def cron_data(self):
        config = self.config
        if not config.get('MAIN_STATUS'):
            return False

        try:
            wifi_data = self._wifi_data
            station_data = self._station_data

            self.data_wifi(wifi_data)
            self.data_station(station_data)
        except ValueError:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False
