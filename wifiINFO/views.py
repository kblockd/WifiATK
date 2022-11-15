# -*- coding: utf-8
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


class Index_api(View):
    @staticmethod
    def get(request):
        try:
            active_wifis = Activelog.objects.count()
            active_clients = []
            for active in Activelog.objects.all().values('client'):
                client = active["client"]
                if client is not None:
                    active_clients.append(client.split(','))
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
            active_clients = active_clients.count()
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

        except Exception as e:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False


class Active_api(View):
    def get(self, request):
        try:
            model = Activelog.objects.all().order_by(
                F('essid').asc(nulls_last=True), F('client').asc(nulls_last=True)).values()

            data = dict()
            data["data"] = list(model)
            return JsonResponse(data, safe=False)
        except:
            return False

    def post(self, request):
        try:
            model = Activelog.objects.all().order_by(
                F('essid').asc(nulls_last=True), F('client').asc(nulls_last=True)).values()

            data = dict()
            data["data"] = list(model)
            return JsonResponse(data, safe=False)
        except:
            return False


class Wifi_api(View):
    def get(self, request):
        try:
            model = Wifilog.objects.all().order_by('bssid').values()

            data = dict()
            data["data"] = list(model)
            return JsonResponse(data, safe=False)
        except:
            return False

    def post(self, request):
        try:
            model = Wifilog.objects.all().order_by('bssid').values()
            data = dict()
            data["data"] = list(model)
            return JsonResponse(data, safe=False)
        except:
            return False


class Station_api(View):
    def get(self, request):
        try:
            model = Stationlog.objects.all().order_by('client').values()

            data = dict()
            data["data"] = list(model)
            return JsonResponse(data, safe=False)
        except:
            return False

    def post(self, request):
        try:
            model = Stationlog.objects.all().order_by('client').values()
            data = dict()
            data["data"] = list(model)
            return JsonResponse(data, safe=False)
        except:
            return False


def attack(request, wifi_bssid):
    if 'start' in request.path_info:
        try:
            target = Activelog.objects.get(bssid=wifi_bssid)
            pid = attacker.AttackManager().deauth(target.bssid, target.channel).pid

            data = dict()
            data["data"] = {"success": 1, "pid": pid}

            return JsonResponse(data, safe=False)

        except:
            data = dict()
            data["data"] = {"success": 0}
            return JsonResponse(data,safe=False)

    if 'stop' in request.path_info:
        try:
            pid = config.get('ATK_PID')
            os.kill(pid,signal.SIGKILL)

            data = dict()
            data["data"] = {"success": 1}
            return JsonResponse(data, safe=False)
        except:
            data = dict()
            data["data"] = {"success": 0}
            return JsonResponse(data, safe=False)


class Config_api(View):

    def get(self, request):
        model = Settings.objects.all()
        data_s = dict()
        for temp in model:
            data_s[temp.key] = temp.value
        data = dict()
        data["data"] = data_s
        return JsonResponse(data, safe=False)

    @staticmethod
    def set(self, request, key, value):
        try:
            config.set()
            data = dict()
            data["data"] = {"success": 1}
            return JsonResponse(data, safe=False)
        except:
            data = dict()
            data["data"] = {"success": 0}
            return JsonResponse(data, safe=False)


def UI(request):
    return render(request, 'dist/index.html')
