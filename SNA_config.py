# -*- coding: utf-8 -*-
#데이터베이스 OID 및 환경 값

DB_HOST = '192.168.0.90' #DB서버위치
DB_PORT= 3306
#DB접속에 필요한 정보
DB_USER='SNA'
DB_PASSWD='smart123'
DB_NAME='SNA'
#SNMP정보를 가져올 주소 및 커뮤니티 ,포트
SNMP_COMMUNITY='smart123'
SNMP_PORT='161'

warning_grade = 0.3
minor_grade = 0.45
major_grade = 0.6
critical_grade = 0.75

SNMP_COLLECT_OIDS=[
    #Equipment
    # '.1.3.6.1.2.1.4.20.1.1',# ipAdEntAddr
    # '.1.3.6.1.2.1.1.5', #sysName
    # '.1.3.6.1.2.1.1.1', #sysDescr
    # '.1.3.6.1.2.1.1.6', #sysLocation

    #Information
    '.1.3.6.1.2.1.2.2.1.1',         # ifIndex
    '.1.3.6.1.2.1.31.1.1.1.4',      # ifName
    '.1.3.6.1.2.1.2.2.1.2',         # ifDescr
    '.1.3.6.1.2.1.31.1.1.1.15',     # ifHighSpeed

    #INPACKET
    '1.3.6.1.2.1.31.1.1.1.6',       # ifHCInOctets  
    '1.3.6.1.2.1.31.1.1.1.7',       # ifHCInUcastPkts
    '1.3.6.1.2.1.31.1.1.1.8',       # ifHCInMulticastPkts
    '1.3.6.1.2.1.31.1.1.1.9',       # ifHCInBroadcastPkts

    #OUTPAKECT
    '1.3.6.1.2.1.31.1.1.1.10',      # ifHCOutOctets
    '1.3.6.1.2.1.31.1.1.1.11',      # ifHCOutUcastPkts
    '1.3.6.1.2.1.31.1.1.1.12',      # ifHCOutMulticastPkts
    '1.3.6.1.2.1.31.1.1.1.13',      # ifHCOutBroadcastPkts

    # #STATUS
    # '.1.3.6.1.2.1.2.2.1.7',         # ifAdminStatus
    # '.1.3.6.1.2.1.2.2.1.8'          # ifOperStatus
]

SNMP_COLLECT_OIDS_DICT = {
    # #Equipment
    # 'ipAdEntAddr':'.1.3.6.1.2.1.4.20.1.1',
    # 'sysDescr':'.1.3.6.1.2.1.1.1',
    # 'sysName' :'.1.3.6.1.2.1.1.5',
    # 'sysLocation':'.1.3.6.1.2.1.1.6',
    
    #Information
    'ifIndex':'.1.3.6.1.2.1.2.2.1.1',
    'ifName':'.1.3.6.1.2.1.31.1.1.1.4', 
    'ifDescr':'.1.3.6.1.2.1.2.2.1.2',
    'ifHighSpeed':'.1.3.6.1.2.1.31.1.1.1.15',

    #INPACKET
    'ifHCInOctets':'1.3.6.1.2.1.31.1.1.1.6',
    'ifHCInUcastPkts':'1.3.6.1.2.1.31.1.1.1.7',
    'ifHCInMulticastPkts':'1.3.6.1.2.1.31.1.1.1.8',
    'ifHCInBroadcastPkts':'1.3.6.1.2.1.31.1.1.1.9',

    #OUTPAKECT
    'ifHCOutOctets':'1.3.6.1.2.1.31.1.1.1.10',
    'ifHCOutUcastPkts':'1.3.6.1.2.1.31.1.1.1.11',
    'ifHCOutMulticastPkts':'1.3.6.1.2.1.31.1.1.1.12',
    'ifHCOutBroadcastPkts':'1.3.6.1.2.1.31.1.1.1.13',

    # #STATUS
    # 'ifAdminStatus':'.1.3.6.1.2.1.2.2.1.7',
    # 'ifOperStatus':'.1.3.6.1.2.1.2.2.1.8'
}

#OID이름을 알아내는 함수
def GET_OIDNAME(oid):
    for k, v in SNMP_COLLECT_OIDS_DICT.items():
        if oid == v:
            return k

#이름으로 코드을 알아내는 함수
def GET_OID(name):
    for k, v in SNMP_COLLECT_OIDS_DICT.items():
        if name == k:
            return v
            
            
SNMP_COUNT_OID = '1.3.6.1.2.1.2.1.0'

#OID데이터를 목록불러오기
SNMP_DATA_DIR = './data'
SNMP_DATA_FILENAME = 'snmp_data.dml'

#수집 주기 (1분)
TRF_PERIOD = 60