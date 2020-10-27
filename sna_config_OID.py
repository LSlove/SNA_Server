
# def GET_OIDNAME(oid):
#     for k, v in SNMP_COLLECT_OIDS_DICT.items():
#         if oid == v:
#             return k

# SNMP_COUNT_OID = '1.3.6.1.2.1.2.1.0'

# SNMP_DATA_DIR = './data'
# SNMP_DATA_FILENAME = 'snmp_data.dml'

# LOG_NAME = 'dml_snmp_trf_collector'
# LOG_DIR = './log'

# TRF_PERIOD = 60

SNA_COLLECT_OIDS=[
    '.1.3.6.1.2.1.1.1', #sysDescr
    '.1.3.6.1.2.1.1.5', #sysName
    '.1.3.6.1.2.1.1.6', #sysLocation

]

SNA_COLLECT_OIDS_DICT={
    'sysDescr': '.1.3.6.1.2.1.1.1',
    'sysName' : '.1.3.6.1.2.1.1.5',
    '#sysLocation': '.1.3.6.1.2.1.1.6'

}
