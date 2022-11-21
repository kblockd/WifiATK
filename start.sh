#!/bin/bash

set -e
plat=$(uname -a |awk '{print $2}')
networkflag=0

if [[ $EUID -ne 0 ]]; then
    echo "权限需要提升:该安装程序必须由root用户执行" 1>&2
		exit 255
fi

if [ "$plat" != "kali" ] && [ "$plat" != "debian" ] && [ "$plat" != "ubuntu" ] && [ "$plat" != "raspberrypi" ];then
  echo "Only Support Debian Family Platform!"
  exit 255
fi


##########
#静态网络#
##########
init_network(){
  if [ "$plat" = "kali" ] || [ "$plat" = "debian" ] || [ "$plat" = "ubuntu" ];then
	  sudo systemctl stop NetworkManager
	  sudo systemctl disable NetworkManager
	fi

	if [ "$plat" = "raspberrypi" ] ; then
	  read -p "请输入默认连接的Wi-Fi名称:" essid
	  read -p "请输入默认连接的Wi-Fi密码：" wifipass
    wifi="wpa-essid $essid
wpa-psk $wifipass"

    sudo systemctl disable avahi-daemon && systemctl stop avahi-daemon
	  sudo systemctl disable dhcpcd && systemctl stop dhcpcd
	  sudo systemctl disable wpa_supplicant && systemctl stop wpa_supplicant

	  cat > /etc/network/interfaces <<EOF ## tab会被读入导致错误
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet dhcp

auto wlan0
iface wlan0 inet dhcp
$wifi
EOF

    sudo ip addr flush dev wlan0
    sudo ifup --ignore-errors wlan0

	else  # X86
	  temp=$(ip route show |grep default |grep eth0 | awk '{printf("ip=%s; gateway=%s;",$9,$3)}')
	  eval "$temp"

	  sudo systemctl disable avahi-daemon && systemctl stop avahi-daemon
	  sudo systemctl disable dhcpcd && systemctl stop dhcpcd
	  sudo systemctl disable wpa_supplicant && systemctl stop wpa_supplicant

	  sudo rm /etc/network/if-up.d/wpasupplicant
    sudo rm /etc/network/if-pre-up.d/wpasupplicant

	  sudo systemctl restart networking

	  cat > /etc/network/interfaces <<EOF ## tab会被读入导致错误
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address $ip
netmask 255.255.255.0
gateway $gateway
EOF

    sudo ip addr flush dev eth0

	fi

  sudo systemctl enable networking
	sudo systemctl restart networking
	echo "nameserver 114.114.114.114" >> /etc/resolv.conf
	echo "nameserver 223.6.6.6" >> /etc/resolv.conf
	cat > /etc/apt/sources.list << EOF
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free
EOF

}

##############
#安装基础软件#
##############
init_soft(){
  cd /opt/Wifi/

	sudo apt install git vim nginx mariadb-server uwsgi uwsgi-plugin-python3 python3 python3-pip tmux  -y
	sudo apt install dnsmasq hostapd bc build-essential dkms mdk4 aircrack-ng -y
	sudo apt install libnl-3-dev libnl-genl-3-dev libssl-dev postfix -y
	sudo pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
	sudo pip3 install virtualenv

	sudo git clone https://ghproxy.com/https://github.com/wifiphisher/roguehostapd.git
	cd roguehostapd
	sudo sed -i "s/ext_modules/entry_points={\n\t\'console_scripts\': [\n\t\t\'roguehostapd = roguehostapd.run\'\n\t]},\n\text_modules/g" setup.py
	sudo sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
  sudo systemctl restart ssh
	sudo python3 setup.py install
	cd  ..
}

##########
#安装驱动#
##########
init_kernel() {
	cd /opt/Wifi/
  sudo git clone https://ghproxy.com/https://github.com/cilynx/rtl88x2bu
	cd rtl88x2bu

  if [ "$plat" = "kali" ] || [ "$plat" = "debian" ] || [ "$plat" = "ubuntu" ] ; then
	  # shellcheck disable=SC2046
	  sudo apt install -y  linux-headers-$(uname -r) ####如果编译报错,可能是因为当前内核与编译库版本对不上，重启后重新执行脚本
	elif [ "$plat" = "raspberrypi" ] ; then
	  # Configure for RasPi
	  sudo apt install -y raspberrypi-kernel-headers
    sed -i 's/I386_PC = y/I386_PC = n/' Makefile
    sed -i 's/ARM_RPI = n/ARM_RPI = y/' Makefile
  fi

	VER=$(sed -n 's/\PACKAGE_VERSION="\(.*\)"/\1/p' dkms.conf)
	sudo rsync -rvhP ./ /usr/src/rtl88x2bu-"${VER}"
	sudo dkms add -m rtl88x2bu -v "${VER}"
	sudo dkms build -m rtl88x2bu -v "${VER}"
	sudo dkms install -m rtl88x2bu -v "${VER}"
	sudo modprobe 88x2bu
}

##########
#虚拟环境#
##########
init_env(){
	cd /opt/Wifi/
	sudo git clone https://ghproxy.com/https://github.com/kblockd/WifiATK.git
	cd WifiATK

	sudo virtualenv venv
	virtual="$(pwd)/venv/bin"
	sudo "$virtual"/pip3 install -r requirements.txt

  echo "SHELL=/bin/bash" >> /var/spool/cron/crontabs/root
  echo "PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin" >> /var/spool/cron/crontabs/root
}

############
#数据库生成#
############
init_database(){
	cd /opt/Wifi/WifiATK/
	virtual="$(pwd)/venv/bin"

	sudo sed -i  's/bind-address            = 127.0.0.1/bind-address            = 0.0.0.0/' /etc/mysql/mariadb.conf.d/50-server.cnf
	sudo systemctl enable mysql
	sudo systemctl start mysql

	#randompass=$(echo $RANDOM | md5sum | head -c 20)
	sqlpass="WifiAttack123."

	cat > ./start.sql <<EOF
CREATE DATABASE Wifi DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE USER 'wifi'@'localhost' IDENTIFIED BY '$sqlpass';
CREATE USER 'wifi'@'%' IDENTIFIED BY '$sqlpass';

GRANT ALL ON Wifi.* TO 'wifi'@'localhost';
GRANT ALL ON Wifi.* TO 'wifi'@'%';
EOF
  #sudo sed -i 's/DEFAULT_SQLPASS/$randompass/' WifiATK/settings.py

	mysql -u root < start.sql
	sudo rm start.sql
	sudo systemctl restart mysql

	sudo "$virtual"/python3 manage.py makemigrations
	sudo "$virtual"/python3 manage.py migrate
	sudo "$virtual"/python3 manage.py crontab add
}

##########
#启动程序#
##########
sstart(){
	cd /opt/Wifi/WifiATK/
	cwd=$(pwd)
	virtual="$cwd/venv/bin"
		cat > /etc/systemd/system/uwsgi.service << EOF
[Unit]
Description=uwsgi
After=mysqld.service
Requires=mysqld.service

[Service]
Type=forking
WorkingDirectory=/opt/Wifi/WifiATK
PIDFile=/var/run/uwsgi.pid
Restart=always
KillSignal=SIGQUIT
StandardError=syslog
NotifyAccess=all

ExecStartPre=bash -c 'cd /opt/Wifi/WifiATK/; git reset --hard master && git pull  --force'
ExecStart=/opt/Wifi/WifiATK/venv/bin/uwsgi --ini /opt/Wifi/WifiATK/uwsgi.ini
ExecReload=/usr/bin/uwsgi --reload /var/run/uwsgi.pid
ExecStop=/usr/bin/uwsgi --stop /var/run/uwsgi.pid

[Install]
WantedBy=multi-user.target

EOF

  sudo systemctl daemon-reload
  sudo systemctl start uwsgi
  sudo systemctl enable uwsgi

}
########
#主函数#
########
main(){
	sudo mkdir -p /opt/Wifi/
	if [ $networkflag = 0 ];then
	  init_network
	  sudo apt update && apt upgrade -y
	  sed -i "s/^networkflag=0/networkflag=1/" "$(realpath "$0")"
	  reboot
	fi

	init_soft
	init_kernel
	init_env
	init_database
	sstart
}

main