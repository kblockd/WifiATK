#!/usr/bin/env python
# -*- coding: utf-8
import hashlib
import os
import re
import linecache
import subprocess
from threading import Thread


#执行命令
def run_cmd(command_list):
    command = ' '.join(command_list)
    ret = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
                         timeout=1)
    if ret.returncode == 0:
        return ret.stdout
    else:
        print(ret.stderr)
        return False


#文件解析
def file_parse(file):
    inputfile = file  ## 输入源文件
    fp = open(inputfile, 'r')
    keyword = 'Station'  ## 切分的关键字
    count = 1

    for each_line in fp:
        m = re.search(keyword, each_line)  ## 查询关键字
        if m is not None:
            key_number = count  # 将关键字的行号
        count += 1

    line_numbers = count + 1  # 文件总行数

    wifi_lines = linecache.getlines(inputfile)[2:key_number - 1]
    station_lines = linecache.getlines(inputfile)[key_number:line_numbers]
    fp.close()

    return (wifi_lines, station_lines)


"""列表对比输出"""
def get_append(oldlist,newlist):

    append = [x for x in newlist if x not in oldlist]
    return append

"""字典集转列表"""
def get_dictkey_list(list_name,**kargs):

    temp_list = []
    for temp in list_name:
        temp_value = ''
        for key in kargs:
            temp_value = temp_value+str(temp[key])
        temp_list.append(
            temp_value
        )

    return temp_list


def list_select(temp_list, **kwargs):

    for temp_dict in temp_list:
        for kwg in kwargs:
            if kwargs[kwg] == temp_dict[kwg]:
                flag =True
                break
            else:
                flag =False
        else:
            continue
        break

    if flag:
        return temp_dict
    else:
        return False

    # for kwg in kwargs:
    #     for temp_dict in temp_list:
    #         print(temp_dict)
    #         print(kwargs[kwg])
    #         if temp_dict.get(kwg) != kwargs[kwg]:
    #             return False
    # return temp_dict


def is_null(value):
    if value == '':
        return None
    else:
        return value


def validate_mac(value):
    # if value.find('-') != -1:
    #     pattern = re.compile(r"^\s*([0-9a-fA-F]{2,2}-){5,5}[0-9a-fA-F]{2,2}\s*$")
    #     if pattern.match(value):
    #         return True
    #     else:
    #         return False
    if value.find(':') != -1:
        pattern = re.compile(r"^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$")
        if pattern.match(value):
            return True
        else:
            return False


def remove_files(file):
    """删除目录下有关键词文件"""
    for temp in os.listdir('.'):
        if file in temp:
            os.remove(temp)


def myasync(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


if __name__ == "__main__":
    pass
# wifi_lines,station_lines =  fileparse('meituan-01.csv')

# print(get_interfaces())
# print(runcmd("ifconfig").stdout)
# Wifis = get_wifi(wifi_lines)
# Stations = get_station(station_lines)
