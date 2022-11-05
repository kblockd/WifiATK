from django.shortcuts import render
from django.views import View
from wifiINFO.wifi import *
"""
------------------------------------------------------------------------------------------
View类
------------------------------------------------------------------------------------------
"""


class Mywifi(View):
    def get(self,request):
        return render(request,'wifi.html')

    def post(self,request):
        return render(request,'wifi.html')


class Mystation(View):
    def get(self,request):
        return render(request,'station.html')

    def post(self,request):
        return render(request,'station.html')


def runoob(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'runoob.html', context)