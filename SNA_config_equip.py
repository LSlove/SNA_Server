
SNMP_COLLECT_OIDS=[
    #Equipment
    ' .1.3.6.1.2.1.4.20.1.1',# ipAdEntAddr
    '.1.3.6.1.2.1.1.5', #sysName
    '.1.3.6.1.2.1.1.1', #sysDescr
    '.1.3.6.1.2.1.1.6', #sysLocation

]

SNMP_COLLECT_OIDS_DICT = {
    #Equipment
    'ipAdEntAddr':'' .1.3.6.1.2.1.4.20.1.1'
    'sysDescr': '.1.3.6.1.2.1.1.1',
    'sysName' : '.1.3.6.1.2.1.1.5',
    'sysLocation': '.1.3.6.1.2.1.1.6',
    
    
}

#OID이름을 알아내는 함수
def GET_OIDNAME(oid):
    for k, v in SNMP_COLLECT_OIDS_DICT.items():
        if oid == v:
            return k

SNMP_COUNT_OID = '1.3.6.1.2.1.2.1.0'

#OID데이터를 목록불러오기
SNMP_DATA_DIR = './data'
SNMP_DATA_FILENAME = 'snmp_data.dml'

#수집 주기 (1분)
TRF_PERIOD = 60