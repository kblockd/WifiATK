# -*- coding: utf-8 -*-
import os
import re
import logging
import configparser
import pyric.pyw
import pyric.pyw as pyw

from wifiINFO.models import Conf
from wifiINFO.common.interfaces import NetworkAdapter

logger = logging.getLogger("wifiINFO.config")


class ConfigManager(object):

    def __init__(self):

        parser = configparser.ConfigParser()
        parser.read('config.ini')
        self._LOGNAME = parser.get('LOG', 'LOGNAME')
        self._LOGDIR = os.getcwd()

        try:
            self._LOG = "{}/{}-01.csv".format(self._LOGDIR, self._LOGNAME)
        except NameError:
            logger.error('Name')
            raise NameError

        self._MONFACE = None
        self._ATKFACE = None
        self._HOSTFACE = None
        self._interfaces = self.get_interfaces()

        self._HOST_PID = None
        self._DNSMASQ_PID = None

        self._MAIN_STATUS = None
        self._ATK_STATUS = parser.get('STATUS', 'ATK_STATUS')

    def initialize(self):
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
            Conf.objects.filter(id=1).update(
                LOGNAME=self._LOGNAME,
                LOGDIR=self._LOGDIR,
                LOG=self._LOG,
                MONFACE=MONFACE_NAME,
                ATKFACE=ATKFACE_NAME,
                HOSTFACE=HOSTFACE_NAME,
                HOST_PID=self._HOST_PID,
                DNSMASQ_PID=self._DNSMASQ_PID,
                MAIN_STATUS=self._MAIN_STATUS,
                ATK_STATUS=self._ATK_STATUS
            )
            return True
        except KeyError:
            return False

    def set(self, **kwargs):
        try:
            update_list = {}
            for key in kwargs.keys():
                if self.has_field(key):
                    update_list[key] = kwargs[key]

            Conf.objects.update(**update_list)

        except KeyError as e:
            print(e)

    @staticmethod
    def has_field(field):
        try:
            Conf._meta.get_field(field)
            return True
        except KeyError:
            print(field + '不存在\r\n')
            return False

    def get(self, key):
        try:
            if self.has_field(key):
                return Conf.objects.filter(id=1).values().first()[key]

        except KeyError:
            print('读取' + key + '失败\r\n')

    # @staticmethod
    def on_exit(self):
        self.set(
            LOGNAME=None,
            LOGDIR=None,
            LOG=None,
            MONFACE=None,
            ATKFACE=None,
            HOSTFACE=None,
            HOST_PID=None,
            DNSMASQ_PID=None,
            MAIN_STATUS=False,
            ATK_STATUS=False
        )

    @staticmethod
    def get_interfaces():
        interfaces = dict()
        faces_name = ['MONFACE', 'ATKFACE', 'HOSTFACE']

        count = 0
        for interface in pyw.interfaces():
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

    @property
    def log(self):
        return self._LOG
