# -*- coding: utf-8
import os
import signal
import traceback
import json
import datetime

from django.views import View
from django.db.models import F
from django.core import serializers
from django.shortcuts import render
from django.http import JsonResponse

from wifiINFO.common import config as configer
from wifiINFO.common import attacker
from wifiINFO.models import Wifilog, Stationlog, Activelog, Conf

config = configer.ConfigManager()


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


class Table(View):
    def count_pages(self, pagesize):
        counts = Wifilog.objects.count()
        if (counts % pagesize == 0):
            pagescount = counts / pagesize
        else:
            pagescount = counts / pagesize + 1
        return pagescount

    def return_data(self):
        #pagesize = self.pagesize
        # currentpage = self.currentpage
        # pagescount = self.count_pages(pagesize)
        query = Wifilog.objects

        # startRow = (currentpage - 1) * pagesize
        # endRow = currentpage * pagesize

        results = query.values('id', 'bssid', 'essid', 'channel', 'privacy'
                              , 'cipher', 'authentication', 'first_time', 'last_time')#[startRow:endRow]
        return results

    def get(self,request, *args, **kwargs):
        wifi_list = self.return_data()
        return render(request, 'table2.html',{'wifi_list':wifi_list})
        # self.pagesize = 25
        # self.currentpage = 2

    def post(self, request, *args, **kwargs):

        return render(request, 'table2.html')


def attack(request, atkid):
    try:
        wifi = Wifilog.objects.filter(id=atkid).values().get()
        # if wifi['bssid'] in :
        #     cron_atk
        return JsonResponse(wifi)
    except Exception as e:
        print('\n', '>>>' * 20)
        print(traceback.print_exc())
        print('\n', '>>>' * 20)
        print(traceback.format_exc())
        return False


class Index(View):
    def get(self,request):
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

            data_list = {
                "active_wifis": active_wifis,
                "active_clients": active_clients,
                "wifi_logs": wifi_logs,
                "station_logs": station_logs,
            }
        except Exception as e:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False
        return render(request, 'index.html', {"data_list": data_list})

    def post(self,request):
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

        except Exception as e:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False
        return render(request, 'index.html', {"data_list": data_list,'atk':atk})


class Index_api(View):
    def get(self,request):
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

        except Exception as e:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False


    def post(self,request):
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


class Active(View):
    def get(self,request):
        try:
            active_data = Activelog.objects.all().order_by(
                F('essid').asc(nulls_last=True), F('client').asc(nulls_last=True)).values()
        except:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False

        return render(request, 'active.html', {'active_data': active_data})

    def post(self,request):
        try:
            active_data = Activelog.objects.all().order_by(
                F('essid').asc(nulls_last=True)).values()
        except:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False
        return render(request, 'active.html', {'active_data': active_data})


class Wifi(View):
    def get(self,request):
        try:
            wifi_data = Wifilog.objects.all().order_by('bssid').values()
        except:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False
        return render(request, 'wifilog.html',{'wifi_data':wifi_data})

    def post(self,request):
        try:
            wifi_data = Wifilog.objects.all().order_by('bssid').values()
        except:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False
        return render(request, 'wifilog.html',{'wifi_data':wifi_data})


class Station(View):
    def get(self, request):
        try:
            station_data = Stationlog.objects.all().order_by('client').values()
        except:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False
        return render(request, 'stationlog.html', {'station_data': station_data})

    def post(self, request):
        try:
            station_data = Stationlog.objects.all().order_by('client').values()
        except:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
            return False
        return render(request, 'stationlog.html', {'station_data': station_data})


def attack(request, wifi_id):
    if 'start' in request.path_info:
        try:
            target = Activelog.objects.get(id=wifi_id)
            pid = attacker.AttackManager().deauth(target.bssid, target.channel).pid

            data = dict()
            data["data"] = {"success": 1, "pid": pid}

            return JsonResponse(data, safe=False)

        except:
            data = dict()
            data["data"] = {"success":0}
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
        model = Conf.objects.all().values()

        data = dict()
        data["data"] = list(model)
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