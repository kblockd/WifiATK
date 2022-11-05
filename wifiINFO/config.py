# -*- coding: utf-8 -*-
from wifiINFO.models import Conf


def _init():  # 初始化
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    # 定义一个全局变量
    # _global_dict[key] = value
    #temp = Conf.objects.get(id=1)
    Conf.objects.filter(id=1).update(**{key:value})
    # temp[key] = value
    # temp.save()


def get_value(key):
    # 获得一个全局变量，不存在则提示读取对应变量失败
    try:
        # if key in _global_dict.keys():
        #     return _global_dict[key]
        # else:
        return Conf.objects.filter(id=1).values(key).first()[key]
    except:
        print('读取' + key + '失败\r\n')


def exit_status():
    Conf.objects.filter(id=1).update(MAIN_STATUS=None)
