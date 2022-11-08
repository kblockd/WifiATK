# -*- coding: utf-8
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from wifiINFO.wifi import *
from wifiINFO.attack import *
from wifiINFO.models import *
from django.db.models import F
from wifiINFO.utils import myasync
import re
"""
------------------------------------------------------------------------------------------
View类
------------------------------------------------------------------------------------------
"""

class Index(View):
    def get(self,request):
        return render(request, 'index.html')

    def post(self,request):
        return render(request, 'index.html')


class Chart(View):
    def get(self,request):
        return render(request, 'chart.html')

    def post(self,request):
        return render(request, 'chart.html')


class Empty(View):
    def get(self,request):
        return render(request, 'empty.html')

    def post(self,request):
        return render(request, 'empty.html')


class Form(View):
    def get(self,request):
        return render(request, 'form.html')

    def post(self,request):
        return render(request, 'form.html')


class Tab_panel(View):
    def get(self,request):
        return render(request, 'tab-panel.html')

    def post(self,request):
        return render(request, 'tab-panel.html')


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

class Ui_elements(View):
    def get(self,request):
        return render(request, 'ui-elements.html')

    def post(self,request):
        return render(request, 'ui-elements.html')


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
        return render(request, 'active.html',{'active_data':active_data})

    def post(self,request):
        try:
            active_data = Activelog.objects.all().order_by(
                F('essid').asc(nulls_last=True)).values()
        except:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
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
        return render(request, 'wifilog.html',{'wifi_data':wifi_data})

    def post(self,request):
        try:
            wifi_data = Wifilog.objects.all().order_by('bssid').values()
        except:
            print('\n', '>>>' * 20)
            print(traceback.print_exc())
            print('\n', '>>>' * 20)
            print(traceback.format_exc())
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

def host_atk(request, wifi_id):
    try:
        pids = start_host(wifi_id)

        return JsonResponse(pids)
    except Exception as e:
        print(e)
