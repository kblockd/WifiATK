#!/bin/bash

set -e

##########
#静态网络#
##########
init_network(){

	sudo systemctl stop NetworkManager
	sudo systemctl disable NetworkManager

	temp=$(ip route show |grep default | awk '{printf("ip=%s; gateway=%s;",$9,$3)}')
	eval $temp

	sudo cat > /etc/network/interfaces <<EOF ## tab会被读入导致错误
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
	sudo systemctl enable networking
	sudo systemctl restart networking
}

##############
#安装基础软件#
##############
init_soft(){
	sudo apt update
	sudo apt install git vim nginx mariadb-server uwsgi python3 python3-pip tmux -y
	sudo apt install dnsmasq hostapd bc build-essential dkms  -y
	sudo apt install libnl-3-dev libnl-genl-3-dev libssl-dev -y
	sudo pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
	sudo pip3 install virtualenv

	sudo git clone https://github.com/wifiphisher/roguehostapd.git
	cd roguehostapd
	sudo sed -i "s/ext_modules/entry_points={\n\t\'console_scripts\': [\n\t\t\'roguehostapd = roguehostapd.run\'\n\t]},\n\text_modules/g" setup.py
	sudo python3 setup.py install
	cd  ..
}

##########
#安装驱动#
##########
init_kernel() {
	cd /opt/Wifi/
	sudo apt install -y  linux-headers-$(uname -r) ####如果编译报错,可能是因为当前内核与编译库版本对不上，重启后重新执行脚本
	sudo git clone https://github.com/cilynx/rtl88x2bu
	cd rtl88x2bu
	VER=$(sed -n 's/\PACKAGE_VERSION="\(.*\)"/\1/p' dkms.conf)
	sudo rsync -rvhP ./ /usr/src/rtl88x2bu-${VER}
	sudo dkms add -m rtl88x2bu -v ${VER}
	sudo dkms build -m rtl88x2bu -v ${VER}
	sudo dkms install -m rtl88x2bu -v ${VER}
	sudo modprobe 88x2bu
	cd ..
}

##########
#虚拟环境#
##########
init_env(){

	cd /opt/Wifi/
	sudo git clone https://github.com/kblockd/WifiATK.git
	cd WifiATK

	sudo virtualenv venv
	virtual="`pwd`/venv/bin"
	sudo $virtual/pip3 install -r requirements.txt
}

############
#数据库生成#
############
init_database(){
	cd /opt/Wifi/WifiATK/
	virtual="`pwd`/venv/bin"

	sudo sed -i  's/bind-address            = 127.0.0.1/bind-address            = 0.0.0.0/' /etc/mysql/mariadb.conf.d/50-server.cnf
	sudo systemctl enable mysql
	sudo systemctl start mysql
	sudo mysql -u root < start.sql

	sudo $virtual/python3 manage.py makemigrations
	sudo $virtual/python3 manage.py migrate
	sudo $virtual/python3 manage.py crontab add
}

##########
#启动程序#
##########
sstart(){
	cd /opt/Wifi/WifiATK/
	virtual="`pwd`/venv/bin"
	sudo nohup $virtual/python3 manage.py runserver 0.0.0.0:8080 --noreload > /tmp/wifi.log 2>&1 &

}
########
#主函数#
########
main(){
	sudo mkdir -p /opt/Wifi/
	init_network
	init_soft
	init_kernel
	init_env
	init_database
	sstart
}


main