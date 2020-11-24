# -*- coding: utf-8 -*-

import json
import os
import sys
from datetime import datetime
import pickle as pk
import numpy as np
import traceback

from sna_snmp import SnaSnmp as snmp
from trf_collector_sql import TrfCollectorSql as sqlExec
import SNA_eq_config as cfg

import threading
import time

SNMP_DEVICE_OIDS=[
    '1.3.6.1.2.1.1.5.0',             #sysName
    '1.3.6.1.2.1.1.1.0',             #sysDescr
    '1.3.6.1.2.1.1.6.0'              #sysLocation
]

SNMP_DEVICE_OIDS_DICT = {
    'sysName' :'1.3.6.1.2.1.1.5',
    'sysDescr':'1.3.6.1.2.1.1.1',
    'sysLocation':'1.3.6.1.2.1.1.6'
}

class SnaEqTrfCollector(object):
    def __init__(self):
        self.snmp = snmp()

    
    #SNMP 데이터 로드
        
    #SNMP_SETTING DATA 받기
    def get_snmp_traffic(self, target, community, oids, count_oid, version=1, timeout=1, retries=3, port=161):
        snmp_data = self.snmp.get_bulk_auto(target, oids, community, count_oid, 
                        version=version, timeout=timeout, retries=retries, port=port)

        return snmp_data

    # def get_snmp_select(self, target, community, oids, count_oid, version, timeout=1, retries=3, port):
    #     snmp_data = self.snmp.get_bulk_auto(target, oids, community, count_oid, 
    #                     version=version, timeout=timeout, retries=retries, port=port)

    #     return snmp_data

    #트래픽 데이터 저장
    def make_save_data(self, target, eq_datas):
        save_eq_data = {} #현재 데이터

        if eq_datas is None: #데이터가 없을 경우
            return None

        #SNMP_DEVICE_OIDS_DICT
        for eq_data_dics in eq_datas:
            for oids, value in eq_data_dics.items() :
                try :
                    # print("oids = ", oids)
                    # print("value = ", value)
                    oid, oid_index = oids.rsplit('.', 1)

                    tmp_dict = {}
                    tmp_dict['IP'] = target
                    #tmp_dict['EQ_INDEX'] = oid_index
                    tmp_dict['OID'] = oid
                    tmp_dict['VALUE'] = value

                    # print("oid : ", oid)
                    # print("oid_index = ", oid_index)
                    # print("target = ", target)
                    # print("Value = ",value)
                    
                    #key = '{0}-{1}-{2}'.format(target, oid_index, oid)
                    key = '{0}-{1}'.format(target, oid)
                    save_eq_data[key] = tmp_dict
                    
                except Exception as e :
                    # print("Exception - ", e)
                    continue
  
        return save_eq_data

    def make_eq_data(self, eq_datas):

      
        device_dict = {}
        for key, cur_data in eq_datas.items():
            try:
                # print ('CUR Data = ', cur_data)
                tmp_dict = {}
                host_key = ('{0}'.format(cur_data['IP']))

                # print('HOST Key = ', host_key )
                try:
                    tmp_dict = device_dict[host_key]
                except KeyError as e:
                    # DB 에 저장할 시간은 일정 시간을 기준으로 저장되어야 함으로 
                    # 저장 기준 간격으로 시간을 정규화 해준다.
                    tmp_dict['IP'] = cur_data['IP']
                    
                finally:
                    
                    if (cur_data['OID'] == SNMP_DEVICE_OIDS_DICT['sysName']) :
                        tmp_dict['EQ_NAME'] = cur_data['VALUE']

                    if (cur_data['OID'] == SNMP_DEVICE_OIDS_DICT['sysDescr']) :
                        tmp_dict['EQ_DESCR'] = cur_data['VALUE']

                    if (cur_data['OID'] == SNMP_DEVICE_OIDS_DICT['sysLocation']) :
                        tmp_dict['EQ_LO'] = cur_data['VALUE']

                device_dict[host_key] = tmp_dict
                #print("device_dict =", device_dict)

            except KeyError as e:
                #print('Not found in previous deviceInfo')
                continue
            except Exception as e :
                # print('Exception occur - ', e)
                # print(" tmp_dict['IP'] = ",  tmp_dict['IP'])
                # print(" tmp_dict['EQ_NAME'] = ",  tmp_dict['EQ_NAME'])
                # print(" tmp_dict['EQ_DESCR'] = ",  tmp_dict['EQ_DESCR'])
                # print(" tmp_dict['EQ_LO'] = ",  tmp_dict['EQ_LO'])
               
                continue

        return device_dict.values()


def main():
    ip_addr = sys.argv[1]
    community = sys.argv[2]
    
    mysql_exec = sqlExec(cfg.DB_HOST, cfg.DB_USER, cfg.DB_PASSWD, cfg.DB_NAME)

    if mysql_exec.conn_db is False:
        print("Can't connect database : check environmnet of database!!!")
        print('END Sna_eq_collector Process!!!')
        return ('','','')
    
    eq_collector = SnaEqTrfCollector()
#---------------------------------------------------------------------
    #targets = mysql_exec.select_equip_target_list()
    #print(targets)

    sys_name = ''
    sys_descr = ''
    sys_location = ''
    
    try:
        eq_data = eq_collector.get_snmp_traffic(ip_addr,
                community,
                SNMP_DEVICE_OIDS_DICT.values(),
                cfg.SNMP_COUNT_OID
        )
        
        #print("eq_data = ", eq_data)
        
        if eq_data is None :
            print("%s : get snmp error" % ip_addr)
            return ('','','')

        save_eq_data = eq_collector.make_save_data(ip_addr, eq_data)
        #print("save_eq_data =", save_eq_data)
        save_eq = eq_collector.make_eq_data(save_eq_data)
        #print(save_eq)
        
        if len(save_eq) > 0 :
            sys_name = save_eq[0]['EQ_NAME']
            sys_descr = save_eq[0]['EQ_DESCR']
            sys_location = save_eq[0]['EQ_LO']
        
        return (sys_name, sys_descr, sys_location)
        
    except Exception as e:
        print(e)
        return ('', '', '')                            

if __name__ == "__main__":
    sys_name, sys_descr, sys_location = main()
    print ('%s|%s|%s' % (sys_name, sys_descr, sys_location))
