# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
import pickle as pk
import numpy as np
import traceback
from pyasn1.type.univ import OctetString
import binascii
#from netaddr import *
from pysnmp.smi import builder
import struct


from sna_snmp import SnaSnmp as snmp
from trf_collector_sql import TrfCollectorSql as sqlExec
import SNA_if_config as cfg

import threading
import time

class SnaIfTrfCollector(object):
    def __init__(self):
        self.snmp = snmp()

    
    #SNMP 데이터 로드
    def load(self, fname, ip_addr):
        snmp_data = None
        filename = ('%s/%s_%s') % (cfg.SNMP_DATA_DIR, fname, ip_addr)

        try:
            with open(filename, 'rb') as f: #파일 로드
                snmp_data = pk.load(f)
            return snmp_data
        except FileNotFoundError as e:#파일을 찾지 못한 경우
            print("FileNotFoundError")
        finally:
            return snmp_data


    def save(self, fname, ip_addr, snmp_data): #snmp 데이터 저장
        if os.path.isdir(cfg.SNMP_DATA_DIR) is False :
            os.makedirs(cfg.SNMP_DATA_DIR)

        filename = ('%s/%s_%s') % (cfg.SNMP_DATA_DIR, fname, ip_addr)
        try:
            with open(filename, 'wb') as f: #파일 입력
                pk.dump(snmp_data, f)
        except Exception as e:
            print("SaveError")
        finally:
            return filename
        
    #SNMP_SETTING DATA 받기
    def get_snmp_traffic(self, target, community, oids, count_oid, version=1, timeout=1, retries=3, port=161):
        snmp_data = self.snmp.get_bulk_auto(target, oids, community, count_oid, 
                        version=version, timeout=timeout, retries=retries, port=port)
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # print("snmp_data",snmp_data)
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return snmp_data

    # def get_snmp_select(self, target, community, oids, count_oid, version, timeout=1, retries=3, port):
    #     snmp_data = self.snmp.get_bulk_auto(target, oids, community, count_oid, 
    #                     version=version, timeout=timeout, retries=retries, port=port)

    #     return snmp_data

    #트래픽 데이터 저장
    def make_save_data(self, target, if_datas):
        total_save_if_data = {} #총 데이터
        save_if_data = {} #현재 데이터
        prev_datas = None #이전 데이터

        if if_datas is None: #데이터가 없을 경우
            return None

        # 시간 수집 주기 기준으로 시간 정규화
        timestamp = int(datetime.now().timestamp())

        #SNMP_COLLECT_OIDS_DICT
        for if_data_dics in if_datas:
            for oids, value in if_data_dics.items() :
                try :
                    oid, oid_index = oids.rsplit('.', maxsplit=1)

                    tmp_dict = {}
                    tmp_dict['IP'] = target
                    tmp_dict['IF_INDEX'] = oid_index
                    tmp_dict['TRF_TYPE'] = oid
                    tmp_dict['VALUE'] = value

                    # print(">>>>>")
                    # print("tep_dict : ",tmp_dict)
                    # print("oids : ",oids)
                    # print("value : ",value)
                    # print(">>>>>")

                    # print("target = ", target)
                    # print("oid : ", oid)
                    # print("oid_index = ", oid_index)
                    # print("Value = ",value)
                    
                    key = '{0}-{1}-{2}'.format(target, oid_index, oid)
                    save_if_data[key] = tmp_dict
                    
                except Exception as e :
                    print("Oid Error")
                    continue
  
        return save_if_data

    #트래픽 데이터 정규화
    def make_if_data(self, if_datas):

        # # cur_timestamp 1개와 cur_datas 1개로 이루어진 데이터
        # for cur_timestamp, cur_datas in if_datas.items():
        #     pass

        
        trf_dict = {}
        for key, cur_data in if_datas.items():
            try:
                # print ('CUR Data = ', cur_data)
                tmp_dict = {}
                host_key = ('{0}-{1}'.format(cur_data['IP'], cur_data['IF_INDEX']))

                # print('HOST Key = ', host_key )
                try:
                    tmp_dict = trf_dict[host_key]
                except KeyError as e:
                    # DB 에 저장할 시간은 일정 시간을 기준으로 저장되어야 함으로 
                    # 저장 기준 간격으로 시간을 정규화 해준다.
                    tmp_dict['IP'] = cur_data['IP']
                    tmp_dict['IF_INDEX'] = cur_data['IF_INDEX']
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
                    if (cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifName']) :
                        tmp_dict['IF_NAME'] = cur_data['VALUE']

                    if (cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifPhysAddress']) :
                        # if len(cur_data['VALUE']) > 0 :
                        #     mibBuilder = builder.MibBuilder()
                        #     MacAddress, = mibBuilder.importSymbols('SNMPv2-TC','MacAddress')
                        #     print (">>>> ", cur_data['VALUE'])

                        #     print(">>>>>>> ",binascii.hexlify(cur_data['VALUE'].encode()).decode())
                        #     macAdd =  MacAddress(hexValue=binascii.hexlify(cur_data['VALUE'].encode()).decode().zfill(12))
                        #     print("!!>>>> MAC : ", macAdd)
                        # else:
                        #     print("ADDR NOT EXIST")
                        #     tmp_dict['MAC_ADDR'] = ''   
                        #print(">>>>>> mac addr1 : ",binascii.hexlify(cur_data['VALUE'].encode()).decode(ascii))
                        # if len(cur_data['VALUE']) > 0 :
                        #     print(">> cur_data = ", cur_data, type(cur_data['VALUE']))
                        #     print(">>>>>> mac addr1 : ", ':'.join('%.2x' % x for x in OctetString(hexValue=cur_data['VALUE'])).asNumbers())
                        
                        tmp_dict['MAC_ADDR'] = binascii.hexlify(cur_data['VALUE'].encode())
                        # if len(cur_data['VALUE']) > 0 :
                        #     print("OctetString : ",OctetString(hexValue=cur_data['VALUE']).asNumbers())
                        #     tmp_dict['MAC_ADDR'] = ':'.join('%.2x' % x for x in OctetString(hexValue=cur_data['VALUE']).asNumbers())
                        #     print("!! tmp_dict['MAC_ADDR'] = ",  tmp_dict['MAC_ADDR'])
                        # else :
                        #     print("ADDR NOT EXIST")
                        #     tmp_dict['MAC_ADDR'] = ''

                    if (cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifAlias']) :
                        tmp_dict['IF_ALIAS'] = cur_data['VALUE']

                    if (cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifDescr']) :
                        tmp_dict['IF_DESCR'] = cur_data['VALUE']

                    if (cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifHighSpeed']) :
                        if cur_data['VALUE'] == 0 :
                            tmp_dict['IF_SPEED'] = cfg.DEFAULT_SPEED
                        else :
                            tmp_dict['IF_SPEED'] = int(cur_data['VALUE']) * cfg.HIGH_SPEED

                    if (cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifAdminStatus']) :
                        tmp_dict['ADMIN_STATUS'] = int(cur_data['VALUE'])

                    if (cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifOperStatus']) :
                        tmp_dict['OPER_STATUS'] = int(cur_data['VALUE'])

                    # tmp_dict['IF_NAME'] = cur_data['ifName']
                    # tmp_dict['ALIAS'] = cfg.SNMP_COLLECT_OIDS_DICT['ifAlias']
                    # tmp_dict['DESCR'] = cfg.SNMP_COLLECT_OIDS_DICT['ifDescr']
                    # tmp_dict['SPEED'] = cfg.SNMP_COLLECT_OIDS_DICT['ifHighSpeed']
                    # tmp_dict['ADMIN_STATUS'] = cfg.SNMP_COLLECT_OIDS_DICT['ifAdminStatus']
                    # tmp_dict['OPER_STATUS'] = cfg.SNMP_COLLECT_OIDS_DICT['ifOperStatus']


                trf_dict[host_key] = tmp_dict
                print("trf_dict =", trf_dict)
                

            except KeyError as e:
                print('Not found in previous if')
                continue
            except Exception as e :
                print(traceback.format_exc())
                print('Exception occur - ', e)
                print(" tmp_dict['IP'] = ",  tmp_dict['IP'])
                print(" tmp_dict['IF_INDEX'] = ",  tmp_dict['IF_INDEX'])
                print(" tmp_dict['IF_NAME'] = ",  tmp_dict['IF_NAME'])
                print(" tmp_dict['MAC_ADDR'] = ",  tmp_dict['MAC_ADDR'])
                print(" tmp_dict['IF_ALIAS'] = ",  tmp_dict['IF_ALIAS'])
                print(" tmp_dict['IF_DESCR'] = ",  tmp_dict['IF_DESCR'])
                print(" tmp_dict['IF_SPEED'] = ",  tmp_dict['IF_SPEED'])
                print(" tmp_dict['ADMIN_STATUS'] = ",  tmp_dict['ADMIN_STATUS'])
                print(" tmp_dict['OPER_STATUS'] = ",  tmp_dict['OPER_STATUS'])
               
                continue

        return trf_dict.values()


def main():
    print('START Sna_if_collector Process!!!')
    mysql_exec = sqlExec(cfg.DB_HOST, cfg.DB_USER, cfg.DB_PASSWD, cfg.DB_NAME)

    if mysql_exec.conn_db is False:
        print("Can't connect database : check environmnet of database!!!")
        print('END Sna_if_collector Process!!!')
        return
    
    if_collector = SnaIfTrfCollector()
#---------------------------------------------------------------------
    targets = mysql_exec.select_equip_target_list()

    print(targets)

    for target in targets:
        try:
            if_data = if_collector.get_snmp_traffic(target[0],
                    target[1],
                    cfg.SNMP_COLLECT_OIDS_DICT.values(),
                    cfg.SNMP_COUNT_OID
            )
            # print("if_data = ")
            # print(if_data)
            # print

            if if_data is None :
                print("%s : collect traffic error" % target[0])
                continue

            save_if_data = if_collector.make_save_data(target[0], if_data)
              
            print("save_if_data = ")
            print(save_if_data)
            print
            # if_collector.save(cfg.SNMP_DATA_FILENAME, target[0], save_if_data) 
            
            save_if = if_collector.make_if_data(save_if_data)
            print("save_if = ",save_if)
            print('\n')
            save_count = mysql_exec.save_if_list(save_if)
            print("save_count = ", save_count)
            if(save_count == False) :
                print("yes data")
                mysql_exec.update_if_list(save_if)
            else :
                print("no data")
                mysql_exec.save_if_list(save_if)
            mysql_exec.commit()
        except Exception as e:
            print(e)
            continue
            

#-------------------------------------------------------------------
    # prev_snmp_data = trf_collector.load(cfg.SNMP_DATA_FILENAME)
    # save_snmp_data = trf_collector.make_save_data(cfg.SNMP_TARGET, snmp_data, prev_snmp_data)

    

    # trf_collector.save(cfg.SNMP_DATA_FILENAME, save_snmp_data)    

    # save_trf_data = trf_collector.make_if_data(save_snmp_data, prev_snmp_data)
    # mysql_exec.save_snmp_trf_list(save_trf_data)
    # mysql_exec.commit()

    # trf_collector.save(cfg.SNMP_DATA_FILENAME, save_snmp_data)

    # print('>> END : SNMP Collect Target - {0}'.format(cfg.SNMP_TARGET))


if __name__ == "__main__":
    main()
  
