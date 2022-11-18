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

            data = dict()
            data["data"] = list(model)
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

    # def post(self, request):
    #     try:
    #         model = Stationlog.objects.all().order_by('client').values()
    #         data = dict()
    #         data["data"] = list(model)
    #         return JsonResponse(data, safe=False)
    #     except RuntimeError:
    #         return False


class Configapi(View):
    @staticmethod
    def success():
        data = dict()
        data["data"] = {"success": 1}
        return JsonResponse(data, safe=False)

    @staticmethod
    def error():
        data = dict()
        data["data"] = {"success": 0}
        return JsonResponse(data, safe=False)

    @staticmethod
    def get(request):
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
                        return self.success()
                    except RuntimeError:
                        return self.error()
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
                        return self.success()
                    except RuntimeError:
                        return self.error()

            elif action == 'ATK_STATUS':

                if value == 'true':
                    value = True
                elif value == 'false':
                    value = False
                else:
                    raise ValueError
                config.set(ATK_STATUS=value)

                data = dict()
                data["data"] = {"success": 1}
                return JsonResponse(data, safe=False)

            elif action == 'LOGNAME':
                config.set(LOGNAME=value)
                return self.success()
            else:
                config.set(**{key: value})
                return self.success()
        except ValueError:
            return self.error()


def webui(request):
    return render(request, 'dist/index.html')


def attack(request, wifi_bssid):
    if 'start' in request.path_info:
        try:
            target = Activelog.objects.get(bssid=wifi_bssid)
            pid = attacker.AttackManager().deauth(target.bssid, target.channel).pid

            data = dict()
            data["data"] = {"success": 1, "pid": pid}

            return JsonResponse(data, safe=False)
        except RuntimeError:
            print(traceback.print_exc())
            print(traceback.format_exc())

            data = dict()
            data["data"] = {"success": 0}
            return JsonResponse(data, safe=False)

    elif 'stop' in request.path_info:
        try:
            pid = config.get('ATK_PID')
            os.kill(pid, signal.SIGKILL)

            data = dict()
            data["data"] = {"success": 1}
            return JsonResponse(data, safe=False)
        except RuntimeError:
            print(traceback.print_exc())
            print(traceback.format_exc())

            data = dict()
            data["data"] = {"success": 0}
            return JsonResponse(data, safe=False)
