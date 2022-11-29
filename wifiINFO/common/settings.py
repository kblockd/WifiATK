# -*- coding: utf-8 -*-
import importlib
import sys
import re
import logging
import pyric.pyw
import pyric.pyw as pyw

from wifiINFO.models import Settings
from wifiINFO.common.interfaces import NetworkAdapter

logger = logging.getLogger("wifiINFO.config")
importlib.reload(sys)


class ConfigManager(object):

    def __init__(self, loganme='TEST123'):

        self._LOGNAME = loganme

        # self._LOGDIR = os.getcwd()
        self._LOGDIR = '/opt/Wifi/WifiATK'  # 此处bug较多，先硬编码

        try:
            self._LOG = "{}/{}-01.csv".format(self._LOGDIR, self._LOGNAME)
        except NameError:
            logger.error('Name')
            raise NameError

        self._MONFACE = None
        self._ATKFACE = None
        self._HOSTFACE = None
        self._interfaces = self.get_interfaces()

        self._MAIN_PID = None
        self._ATK_BSSID = None
        self._ATK_PID = None
        self._HOST_PID = None
        self._DNSMASQ_PID = None

        self._MAIN_STATUS = False
        self._ATK_STATUS = False

        self._DUMP_BSSID = None
        self._DUMP_PID = None

    def initialize(self):
        # if self.get('MAIN_STATUS') == 'True':
        #     self._MAIN_STATUS = self.get('MAIN_STATUS')
        #     self._ATK_STATUS = self.get('ATK_STATUS')
        #     self._MONFACE = self.get('MONFACE')
        #     self._ATKFACE = self.get('ATKFACE')
        #     self._HOSTFACE = self.get('HOSTFACE')
        #     self._LOG = self.get('LOG')
        #     self._MAIN_PID = self.get('MAIN_PID')
        #     self._ATK_BSSID = self.get('ATK_BSSID')
        #     self._ATK_PID = self.get('ATK_PID')
        #     self._HOST_PID = self.get('HOST_PID')
        #     self._DNSMASQ_PID = self.get('DNSMASQ_PID')


        inters_count = len(self._interfaces)

        if inters_count == 1:
            self._MONFACE = self._interfaces['MONFACE']
            MONFACE_NAME = self._MONFACE.name
            ATKFACE_NAME = None
            HOSTFACE_NAME = None
        elif inters_count == 2:
            self._MONFACE = self._interfaces['MONFACE']
            self._ATKFACE = self._interfaces['ATKFACE']
            MONFACE_NAME = self._MONFACE.name
            ATKFACE_NAME = self._ATKFACE.name
            HOSTFACE_NAME = None
        elif inters_count == 3:
            self._MONFACE = self._interfaces['MONFACE']
            self._ATKFACE = self._interfaces['ATKFACE']
            self._HOSTFACE = self._interfaces['HOSTFACE']
            MONFACE_NAME = self._MONFACE.name
            ATKFACE_NAME = self._ATKFACE.name
            HOSTFACE_NAME = self._HOSTFACE.name
        else:
            raise EOFError

        try:
            self.set(
                MAIN_STATUS=self._MAIN_STATUS,
                ATK_STATUS=self._ATK_STATUS,
                LOGNAME=self._LOGNAME,
                LOGDIR=self._LOGDIR,
                LOG=self._LOG,
                MONFACE=MONFACE_NAME,
                ATKFACE=ATKFACE_NAME,
                HOSTFACE=HOSTFACE_NAME,
                MAIN_PID=self._MAIN_PID,
                ATK_BSSID=self._ATK_BSSID,
                ATK_PID=self._ATK_PID,
                HOST_PID=self._HOST_PID,
                DNSMASQ_PID=self._DNSMASQ_PID,
                DUMP_BSSID=self._DUMP_BSSID,
                DUMP_PID=self._DUMP_PID,
            )
            return self
        except KeyError:
            return False

    @staticmethod
    def get(key):
        try:
            return Settings.objects.get(key=key).value
        except KeyError:
            print('读取' + key + '失败\r\n')
            return False

    def set(self, **kwargs):
        Settings.objects.update_or_create(key="DUMP_BSSID", value=None)
        try:
            update_list = []
            keys = list(kwargs.keys())
            for key in keys:
                data = self.does_has_key(key)
                if data:
                    value = kwargs[key]
                    """Settings Object: """
                    data.value = value

                    update_list.append(
                        data
                    )
                else:
                    continue

            Settings.objects.bulk_update(
                update_list, ['value']
            )
            return True
        except KeyError as e:
            print(e)
            return False

    @staticmethod
    def does_has_key(key):
        try:
            data = Settings.objects.get(key=key)
            return data
        except KeyError:
            print(key + '不存在\r\n')
            return False

    # @staticmethod
    def on_exit(self):
        self.set(
            LOGNAME=None,
            LOGDIR=None,
            LOG=None,
            MONFACE=None,
            ATKFACE=None,
            HOSTFACE=None,
            MAIN_PID=None,
            ATK_BSSID=None,
            ATK_PID=None,
            HOST_PID=None,
            DNSMASQ_PID=None,
            MAIN_STATUS=False,
            ATK_STATUS=False,
            DUMP_BSSID=None,
            DUMP_PID=None,
        )

    @staticmethod
    def get_interfaces():
        interfaces = dict()
        faces_name = ['MONFACE', 'ATKFACE', 'HOSTFACE']

        count = 0
        for interface in pyw.interfaces():
            if interface == 'wlan0':
                continue

            try:
                card = pyw.getcard(interface)
                mac_address = pyw.macget(card)
                adapter = NetworkAdapter(interface, card, mac_address)
                interfaces[faces_name[count]] = adapter
                count += 1
            # ignore devices that are not supported(93) and no such device(19)
            except pyric.error as error:
                if error.args[0] in (93, 19):
                    pass
                elif re.match('^eth|ens', interface):
                    continue
                else:
                    raise error

        if len(interfaces) == 0:
            raise OSError

        return interfaces

    @property
    def interfaces(self):
        return self._interfaces
