# -*- coding: utf-8

import subprocess
from threading import Thread


def run_cmd(command_list):   # 执行命令
    command = ' '.join(command_list)
    ret = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
                         timeout=10)
    if ret.returncode == 0:
        return ret.stdout
    else:
        print(ret.stderr)
        return False


def get_append(oldlist, newlist):
    """列表对比输出"""
    append = [x for x in newlist if x not in oldlist]
    return append


def get_dictkey_list(list_name, **kargs):
    """字典集转列表"""
    temp_list = []
    for temp in list_name:
        temp_value = ''
        for key in kargs:
            temp_value = temp_value+str(temp[key])
        temp_list.append(
            temp_value
        )

    return temp_list


def is_data_null(value):
    if value == '':
        return None
    else:
        return value


def is_mac_validate(mac_address):
    import re

    if mac_address.find(':') != -1:
        pattern = re.compile(r"^\s*([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\s*$")
        if pattern.match(mac_address):
            return True

    return False


def myasync(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


if __name__ == "__main__":
    pass
