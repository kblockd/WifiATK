# coding = utf-8
import os
import subprocess
from wifiINFO import config
import traceback


def iptables_setting(ATKFACE):
    try:
        os.system("sudo ifconfig {} up 172.20.20.1 netmask 255.255.255.0".format(ATKFACE))
        os.system("sudo iptables --flush")
        os.system("sudo iptables --table nat --flush")
        os.system("sudo iptables --delete-chain")
        os.system("sudo iptables --table nat --delete-chain")
        os.system("sudo iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE")
        os.system("sudo iptables -A FORWARD -i eth0 -o {} -m state --state RELATED,ESTABLISH -j ACCEPT".format(ATKFACE))
        os.system("sudo iptables -A FORWARD -i {} -o eth0 -j ACCEPT ".format(ATKFACE))
        os.system("sudo iptables --append FORWARD --in-interface {} -j ACCEPT".format(ATKFACE))
        # /IPTABLES
    except Exception as e:
        print('\n', '>>>' * 20)
        print(traceback.print_exc())
        print('\n', '>>>' * 20)
        print(traceback.format_exc())


def dnsmasq(ATKFACE):
    try:
        os.system("sudo ifconfig {} up".format(ATKFACE))
        # os.system("sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.backup")

        dnsmasq_file = """# disables dnsmasq reading any other files like /etc/resolv.conf for nameservers
no-resolv
# Interface to bind to
interface={}
#Specify starting_range,end_range,lease_time 
dhcp-range=172.20.20.3,172.20.20.20,12h
# dns addresses to send to the clients
# server=8.8.8.8
server=172.20.20.1
server=223.6.6.6\n""".format(ATKFACE)

        open("/etc/dnsmasq.conf", 'w+').write(dnsmasq_file)

    except Exception as e:
        print('\n', '>>>' * 20)
        print(traceback.print_exc())
        print('\n', '>>>' * 20)
        print(traceback.format_exc())

    try:
        # os.system("sudo /etc/init.d/dnsmasq stop > /dev/null 2>&1")
        # os.system("sudo pkill dnsmasq")
        dnsmasq_pid = subprocess.Popen([
            'sudo',
            'dnsmasq',
            '-d'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return dnsmasq_pid

    except Exception as e:
        print('\n', '>>>' * 20)
        print(traceback.print_exc())
        print('\n', '>>>' * 20)
        print(traceback.format_exc())


def hostapd(ATKFACE, essid, channel):
    try:
        # HOSTAPD CONFIG
        hostapd_file = """interface={}
driver=nl80211
ssid={}
hw_mode=g
channel={}
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
""".format(ATKFACE, essid, str(channel))

        open("/etc/hostapd/hostapd.conf", 'w+').write(hostapd_file)

    except Exception as e:
        print('\n', '>>>' * 20)
        print(traceback.print_exc())
        print('\n', '>>>' * 20)
        print(traceback.format_exc())

    try:
        os.system("sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1")
        process = subprocess.Popen([
            'sudo',
            'hostapd',
            '/etc/hostapd/hostapd.conf'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return process

    except Exception as e:
        print('\n', '>>>' * 20)
        print(traceback.print_exc())
        print('\n', '>>>' * 20)
        print(traceback.format_exc())
        pass


def host(essid, channel):
    ATKFACE = config.get_value('ATKFACE')

    iptables_setting(ATKFACE)
    dnsmasq_pid = dnsmasq(ATKFACE)
    host_pid = hostapd(ATKFACE, essid, channel)

    return dnsmasq_pid, host_pid
