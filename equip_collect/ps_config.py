# -*- coding: utf-8 -*-
import datetime

import psutil
import socket, fcntl, struct
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s','eth0'))[20:24])


now=datetime.datetime.now()
nowtime=now.strftime('%Y-%m-%d')#년-원-일
nowDatetime=now.strftime('%Y-%m-%d %H:%M:%S')#년-원-일-시-분-초

cpu=psutil.cpu_percent(interval=None, percpu=False)  #cpu%
memory=psutil.disk_usage('/').percent                #memory%
disk=str((psutil.disk_usage('/').free)/(1024.0 ** 3))[0:7]   #disk %
#ip=socket.gethostbyname(socket.gethostname())

# print({cpu},{memory},{disk},{ip})

DB_host='192.168.0.90'
DB_user='SNA'
DB_password='smart123'
DB_db='SNA'