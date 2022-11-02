from .wifi import  *


def first_start(LOGNAME):
    config._init()
    config.set_value('LOGNAME', LOGNAME)
    #config.set_value('LOG', 'meituan-01.csv')

    LOGNAME = config.get_value('LOGNAME')
    #LOG = LOGNAME+'-01.csv'
    time1 = time.time()
    pid = start_airmon()
    print(pid)
    time2 = time.time()
    print(time2 - time1)

    # count = 0
    # while True:
    #     time.sleep(60)
    #     time1 = time.time()
    #     wifi_lines, station_lines = file_parse(LOG)
    #     data_wifi(wifi_lines)
    #     data_station(station_lines)
    #     count += 1
    #     print(count)
    #     time2 = time.time()
    #     print('消耗:{}'.format(time2-time1))


first_start('meituan')