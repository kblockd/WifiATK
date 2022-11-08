# coding = utf-8
import os
import subprocess

sudo = "/usr/bin/sudo"
tee = "/usr/bin/tee"


def _run_cmd_write(cmd_args, s):
    # write a file using sudo
    p = subprocess.Popen(cmd_args, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, shell=False, universal_newlines=True)
    p.stdin.write(s)
    p.stdin.close()
    p.wait()


def write_file(path, s):
    _run_cmd_write((sudo, tee, path), s)


def dnsmasq(ATKFACE):
    try:
        network_manager_cfg = """
[main]
plugins=keyfile
[keyfile]
unmanaged-devices=interface-name:{}
""".format(ATKFACE)

        os.system("sudo cp /etc/NetworkManager/NetworkManager.conf /etc/NetworkManager/NetworkManager.conf.backup")
        write_file("/etc/NetworkManager/NetworkManager.conf", network_manager_cfg)
        os.system("sudo service NetworkManager restart")
        os.system("sudo ifconfig {ATKFACE} up")
        os.system("sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.backup")

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

        os.system("sudo rm /etc/dnsmasq.conf > /dev/null 2>&1")
        write_file("/etc/dnsmasq.conf", dnsmasq_file)

    except Exception as e:
        print(e)


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
        os.system("sudo rm /etc/hostapd/hostapd.conf > /dev/null 2>&1")
        write_file("/etc/hostapd/hostapd.conf", hostapd_file)
    except Exception as e:
        print(e)


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
        print(e)


def start_dnsmasq():
    try:
        os.system("sudo /etc/init.d/dnsmasq stop > /dev/null 2>&1")
        os.system("sudo pkill dnsmasq")
        os.system("sudo dnsmasq")
    except Exception as e:
        print(e)


def start_hostapd():
    try:
        os.system("sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1")
        process = subprocess.Popen([
            'sudo',
            'hostapd',
            '/etc/hostapd/hostapd.conf'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return process

    except Exception as e:
        print(e)
        pass


def start_apd(ATKFACE, essid, channel):
    dnsmasq(ATKFACE)
    hostapd(ATKFACE, essid, channel)
    iptables_setting(ATKFACE)
    start_dnsmasq()
    process = start_hostapd()
    return process
