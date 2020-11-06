# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime
import pickle as pk
import numpy as np
import traceback

from sna_snmp import SnaSnmp as snmp
from trf_collector_sql import TrfCollectorSql as sqlExec
import SNA_eq_config as cfg

import threading
import time

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

        #SNMP_COLLECT_OIDS_DICT
        for eq_data_dics in eq_datas:
            for oids, value in eq_data_dics.items() :
                try :
                    oid, oid_index = oids.rsplit('.', maxsplit=1)

                    tmp_dict = {}
                    tmp_dict['IP'] = target
                    #tmp_dict['EQ_INDEX'] = oid_index
                    tmp_dict['TRF_TYPE'] = oid
                    tmp_dict['VALUE'] = value

                    # print("target = ", target)
                    # print("oid : ", oid)
                    # print("oid_index = ", oid_index)
                    # print("Value = ",value)
                    
                    #key = '{0}-{1}-{2}'.format(target, oid_index, oid)
                    key = '{0}-{1}'.format(target, oid)
                    save_eq_data[key] = tmp_dict
                    
                except Exception as e :
                    print("Oid Error")
                    continue
  
        return save_eq_data

    #트래픽 데이터 정규화
    def make_eq_data(self, eq_datas):

        # # cur_timestamp 1개와 cur_datas 1개로 이루어진 데이터
        # for cur_timestamp, cur_datas in if_datas.items():
        #     pass

        
        trf_dict = {}
        for key, cur_data in eq_datas.items():
            try:
                # print ('CUR Data = ', cur_data)
                tmp_dict = {}
                host_key = ('{0}'.format(cur_data['IP']))

                # print('HOST Key = ', host_key )
                try:
                    tmp_dict = trf_dict[host_key]
                except KeyError as e:
                    # DB 에 저장할 시간은 일정 시간을 기준으로 저장되어야 함으로 
                    # 저장 기준 간격으로 시간을 정규화 해준다.
                    tmp_dict['IP'] = cur_data['IP']
                    # tmp_dict['IF_NAME'] = cur_data['ifName']
                    # tmp_dict['ALIAS'] = cfg.SNMP_COLLECT_OIDS_DICT['ifAlias']
                    # tmp_dict['DESCR'] = cfg.SNMP_COLLECT_OIDS_DICT['ifDescr']
                    # tmp_dict['SPEED'] = cfg.SNMP_COLLECT_OIDS_DICT['ifHighSpeed']
                    # tmp_dict['ADMIN_STATUS'] = cfg.SNMP_COLLECT_OIDS_DICT['ifAdminStatus']
                    # tmp_dict['OPER_STATUS'] = cfg.SNMP_COLLECT_OIDS_DICT['ifOperStatus']
                finally:
                    print(cur_data['TRF_TYPE'])
                    print(" = ")
                    print(cfg.SNMP_COLLECT_OIDS_DICT['ifName'])
                    if (cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['sysName']) :
                        tmp_dict['EQ_NAME'] = cur_data['VALUE']

                    if (cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['sysDescr']) :
                        tmp_dict['EQ_DESCR'] = cur_data['VALUE']

                    if (cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['sysLocation']) :
                        tmp_dict['EQ_LO'] = cur_data['VALUE']

                trf_dict[host_key] = tmp_dict
                print("trf_dict =", trf_dict)

            except KeyError as e:
                print('Not found in previous if')
                continue
            except Exception as e :
                print('Exception occur - ', e)
                print(" tmp_dict['IP'] = ",  tmp_dict['IP'])
                print(" tmp_dict['EQ_NAME'] = ",  tmp_dict['EQ_NAME'])
                print(" tmp_dict['EQ_DESCR'] = ",  tmp_dict['EQ_DESCR'])
                print(" tmp_dict['EQ_LO'] = ",  tmp_dict['EQ_LO'])
               
                continue

        return trf_dict.values()


def main():
    print('START Sna_eq_collector Process!!!')
    mysql_exec = sqlExec(cfg.DB_HOST, cfg.DB_USER, cfg.DB_PASSWD, cfg.DB_NAME)

    if mysql_exec.conn_db is False:
        print("Can't connect database : check environmnet of database!!!")
        print('END Sna_eq_collector Process!!!')
        return
    
    eq_collector = SnaEqTrfCollector()
#---------------------------------------------------------------------
    targets = mysql_exec.select_equip_target_list()

    print(targets)

    for target in targets:
        try:
            eq_data = eq_collector.get_snmp_traffic(target[0],
                    target[1],
                    cfg.SNMP_COLLECT_OIDS_DICT.values(),
                    cfg.SNMP_COUNT_OID
            )
            # print("if_data = ")
            # print(if_data)
            # print

            if eq_data is None :
                print("%s : collect traffic error" % target[0])
                continue

            save_eq_data = eq_collector.make_save_data(target[0], eq_data)
              
            print("save_if_data = ")
            print(save_eq_data)
            print
            # if_collector.save(cfg.SNMP_DATA_FILENAME, target[0], save_if_data) 
            
            save_eq = eq_collector.make_eq_data(save_eq_data)
            print("save_if = ",save_eq)
            print('\n')
            mysql_exec.update_eq_list(save_eq)
            mysql_exec.commit()
        except Exception as e:
            print(e)
            continue
            

#-------------------------------------------------------------------
    # prev_snmp_data = trf_collector.load(cfg.SNMP_DATA_FILENAME)
    # save_snmp_data = trf_collector.make_save_data(cfg.SNMP_TARGET, snmp_data, prev_snmp_data)

    

    # trf_collector.save(cfg.SNMP_DATA_FILENAME, save_snmp_data)    

    # save_trf_data = trf_collector.make_eq_data(save_snmp_data, prev_snmp_data)
    # mysql_exec.save_snmp_trf_list(save_trf_data)
    # mysql_exec.commit()

    # trf_collector.save(cfg.SNMP_DATA_FILENAME, save_snmp_data)

    # print('>> END : SNMP Collect Target - {0}'.format(cfg.SNMP_TARGET))


if __name__ == "__main__":
    main()
  
