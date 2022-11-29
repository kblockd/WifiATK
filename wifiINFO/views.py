# -*- coding: utf-8
import sys
import importlib
import os
import signal
import traceback

from django.views import View
from django.db.models import F
from django.shortcuts import render
from django.http import JsonResponse

from wifiINFO.common import attacker
from wifiINFO.common import settings as configer
from wifiINFO.models import Wifilog, Stationlog, Activelog, Settings

config = configer.ConfigManager()
importlib.reload(sys)


class Indexapi(View):
    @staticmethod
    def get(request):
        try:
            active_wifis = Activelog.objects.count()
            active_clients = []
            for active in Activelog.objects.all().values('client'):
                client = active["client"]
                if client is not None:
                    active_clients.extend(client.split(','))
            active_clients = len(active_clients)
            wifi_logs = Wifilog.objects.count()
            station_logs = Stationlog.objects.count()

            data = dict()
            data_list = {
                "active_wifis": active_wifis,
                "active_clients": active_clients,
                "wifi_logs": wifi_logs,
                "station_logs": station_logs,
            }
            data["data"] = data_list

            return JsonResponse(data, safe=False)

        except ValueError:

            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False

    @staticmethod
    def post(request):
        try:
            active_wifis = Activelog.objects.count()
            active_clients = []
            for active in Activelog.objects.all().values('client'):
                client = active["client"]
                if client is not None:
                    active_clients = active_clients.append(client.split(','))
            active_clients = len(active_clients)
            wifi_logs = Wifilog.objects.count()
            station_logs = Stationlog.objects.count()

            data = dict()
            data_list = {
                "active_wifis": active_wifis,
                "active_clients": active_clients,
                "wifi_logs": wifi_logs,
                "station_logs": station_logs,
            }
            if config.get('ATKFACE') is None:
                atk = 0
            else:
                atk = 1

            data["data"] = data_list
            data['atk'] = atk

            return JsonResponse(data, safe=False)

        except RuntimeError:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False


class Activeapi(View):
    @staticmethod
    def get(request):
        try:
            model = Activelog.objects.all().order_by(
                F('essid').asc(nulls_last=True), F('client').asc(nulls_last=True)).values()

            data_obj = list(model)
            ATK_STATUS = config.get('ATK_STATUS')
            atking_bssid = config.get('ATK_BSSID')

            dumping_bssid = config.get('DUMP_BSSID')

            for log in data_obj:
                """

                """
                if ATK_STATUS == 'True':
                    log['ATK_FLAG'] = False
                elif log['bssid'] == atking_bssid:
                    log['ATK_FLAG'] = 2
                elif log['bssid'] != atking_bssid:
                    if int(log['power']) > -80:
                        log['ATK_FLAG'] = 1
                    else:
                        log['ATK_FLAG'] = False
                else:
                    log['ATK_FLAG'] = 'Error'

                """
                    
                """

                if ATK_STATUS == 'True':
                    log['DUMP_FLAG'] = False
                elif log['bssid'] == dumping_bssid:
                    log['DUMP_FLAG'] = 2
                elif log['bssid'] != dumping_bssid:
                    if atking_bssid is None:
                        if int(log['power']) > -80:
                            log['DUMP_FLAG'] = 1
                        else:
                            log['DUMP_FLAG'] = False
                    else:
                        if log['bssid'] == atking_bssid:
                            log['DUMP_FLAG'] = 1
                        else:
                            log['DUMP_FlAG'] = False
                else:
                    log['DUMP_FLAG'] = 'Error'

            data = dict()
            data["data"] = data_obj
            """
            {
              "id": 23,
              "bssid": "B0:CC:FE:26:EA:20",
              "essid": "6816901",
              "client": null,
              "channel": "1",
              "privacy": "WPA2 WPA",
              "cipher": "CCMP",
              "authentication": "PSK",
              "power": "-111",
              "ATK_FLAG": 1,
              "DUMP_FLAG": 1
            }
            """
            return JsonResponse(data, safe=False)
        except RuntimeError:
            return False

    # def post(self, request):
    #     try:
    #         model = Activelog.objects.all().order_by(
    #             F('essid').asc(nulls_last=True), F('client').asc(nulls_last=True)).values()
    #
    #         data = dict()
    #         data["data"] = list(model)
    #         return JsonResponse(data, safe=False)
    #     except RuntimeError:
    #         return False


class Wifiapi(View):
    @staticmethod
    def get(request):
        try:
            model = Wifilog.objects.all().order_by('bssid').values()

            data = dict()
            data["data"] = list(model)
            return JsonResponse(data, safe=False)
        except RuntimeError:
            return False

    @staticmethod
    def post(request):
        try:
            model = Wifilog.objects.all().order_by('bssid').values()
            data = dict()
            data["data"] = list(model)
            return JsonResponse(data, safe=False)
        except RuntimeError:
            return False


class Stationapi(View):
    @staticmethod
    def get(request):
        try:
            model = Stationlog.objects.all().order_by('client').values()

            data = dict()
            data["data"] = list(model)
            return JsonResponse(data, safe=False)
        except RuntimeError:
            return False


class Configapi(View):

    def get(self, request):
        model = Settings.objects.all()
        data_s = dict()
        for temp in model:
            data_s[temp.key] = temp.value
        data = dict()
        data["data"] = data_s
        return JsonResponse(data, safe=False)

    def set(self, key, value):

        try:
            action = key

            if action == 'MAIN_STATUS':
                from wifiINFO.common import monitor
                if config.get('MAIN_STATUS') == value:
                    pass
                elif value:
                    try:
                        monitor.MonitorManager().stop()
                        config.set(MAIN_STATUS=value)  # 关闭
                        return success()
                    except RuntimeError:
                        return error()
                else:
                    try:
                        monitor.MonitorManager().start()

                        if value == 'true':
                            value = True
                        elif value == 'false':
                            value = False
                        else:
                            raise ValueError

                        config.set(MAIN_STATUS=value)  # 打开
                        return success()
                    except RuntimeError:
                        return error()

            elif action == 'ATK_STATUS':

                if value == 'true':
                    config.set(ATK_STATUS=True, ATK_PID=None, ATK_BSSID=None)
                    attacker.AttackManager().start_cron()
                    return success()

                elif value == 'false':
                    pid = config.get('ATK_PID')
                    if pid is not None:
                        try:
                            os.kill(pid, signal.SIGKILL)
                        except KeyError:
                            return error()
                    config.set(ATK_STATUS=False, ATK_PID=None, ATK_BSSID=None)
                    return success()

                else:
                    return error()

            elif action == 'LOGNAME':
                config.set(LOGNAME=value)
                return success()
            else:
                # config.set(**{key: value})
                return error()
        except ValueError:
            return error()


def webui(request):
    return render(request, 'dist/index.html')


def attack(request, wifi_bssid):
    atkman = attacker.AttackManager(wifi_bssid)
    if 'start' in request.path_info:
        try:

            if config.get('ATK_PID') is not None:
                return error()

            pid = atkman.attack().pid

            return success(pid=pid)

        except RuntimeError:
            print(traceback.print_exc())
            print(traceback.format_exc())

            return error()

    elif 'stop' in request.path_info:
        try:
            atkman.kill()
            return success()
        except RuntimeError:
            print(traceback.print_exc())
            print(traceback.format_exc())

            return error()


def dump(request, wifi_bssid):
    atkman = attacker.AttackManager(wifi_bssid)
    atkman.dump()
    return success()


def success(**kwargs):
    data = dict()
    data["data"] = {"success": 1}
    for key in kwargs:
        data[key] = kwargs[key]
    return JsonResponse(data, safe=False)


def error(**kwargs):
    data = dict()
    data["data"] = {"success": 0}
    for key in kwargs:
        data[key] = kwargs[key]
    return JsonResponse(data, safe=False)
