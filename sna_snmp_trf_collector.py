# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime
import pickle as pk
import numpy as np
import traceback

from sna_snmp import SnaSnmp as snmp
from trf_collector_sql import TrfCollectorSql as sqlExec
import SNA_config as cfg
import sna_errorEvent

import threading
import time

class SnaSnmpTrfCollector(object):
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

        return snmp_data

    # def get_snmp_select(self, target, community, oids, count_oid, version, timeout=1, retries=3, port):
    #     snmp_data = self.snmp.get_bulk_auto(target, oids, community, count_oid, 
    #                     version=version, timeout=timeout, retries=retries, port=port)

    #     return snmp_data

    #트래픽 데이터 저장
    def make_save_data(self, target, snmp_datas, prev_snmp_datas = None):
        total_save_snmp_data = {} #총 데이터
        save_snmp_data = {} #현재 데이터
        prev_datas = None #이전 데이터

        if snmp_datas is None: #데이터가 없을 경우
            return None

        if prev_snmp_datas is not None : # 데이터가 있을 경우
            for prev_timestamp , prev_datas in prev_snmp_datas.items():
                pass

        # 시간 수집 주기 기준으로 시간 정규화
        timestamp = int(datetime.now().timestamp())

        #SNMP_COLLECT_OIDS_DICT
        for snmp_data_dics in snmp_datas:
            for oids, value in snmp_data_dics.items() :
                try :
                    oid, oid_index = oids.rsplit('.', maxsplit=1)

                    tmp_dict = {}
                    tmp_dict['IP'] = target
                    tmp_dict['SNMP_INDEX'] = oid_index
                    tmp_dict['TRF_TYPE'] = oid
                    tmp_dict['CURR_COUNTER'] = value

                    key = '{0}-{1}-{2}'.format(target, oid_index, oid)

                    try:
                        prev_count = prev_datas[key]['CURR_COUNTER']
                        calc_count = self.snmp.calc_counter64(prev_count, value)
                    except KeyError as e:
                        calc_count = 0
                    except Exception as e:
                        calc_count = 0

                    tmp_dict['CALC_COUNTER'] = calc_count
                    save_snmp_data[key] = tmp_dict

                except Exception as e :
                    continue

        total_save_snmp_data[timestamp] = save_snmp_data
        return total_save_snmp_data

    #트래픽 데이터 정규화
    def make_trf_data(self, snmp_datas, prev_snmp_datas):

        if prev_snmp_datas is None:
            return None

        # cur_timestamp 1개와 cur_datas 1개로 이루어진 데이터
        for cur_timestamp, cur_datas in snmp_datas.items():
            pass

        # prev_timestamp 1개와 prev_datas 1개로 이루어진 데이터
        for prev_timestamp, prev_datas in prev_snmp_datas.items():
            pass

        time_period = cur_timestamp - prev_timestamp

        trf_dict = {}
        for key, cur_data in cur_datas.items():
            try:
                tmp_dict = {}
                host_key = ('{0}-{1}'.format(cur_data['IP'], cur_data['SNMP_INDEX']))

                try:
                    tmp_dict = trf_dict[host_key]
                except KeyError as e:
                    # DB 에 저장할 시간은 일정 시간을 기준으로 저장되어야 함으로 
                    # 저장 기준 간격으로 시간을 정규화 해준다.
                    tmp_dict['IP'] = cur_data['IP']
                    tmp_dict['SNMP_INDEX'] = cur_data['SNMP_INDEX']
                    tmp_dict['TIMESTAMP'] = datetime.fromtimestamp(int(cur_timestamp - (cur_timestamp % cfg.TRF_PERIOD)))
                    tmp_dict['BPS_IN'] = 0
                    tmp_dict['BPS_OUT'] = 0
                    tmp_dict['PPS_IN'] = 0
                    tmp_dict['PPS_OUT'] = 0
                finally:
                    tmp_dict['SNMP_INDEX'] = cur_data['SNMP_INDEX']
                    if (cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifHCInOctets']) :
                        tmp_dict['BPS_IN'] = self.calc_bps(cur_data['CALC_COUNTER'], time_period)
                    elif (cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifHCOutOctets']) :
                        tmp_dict['BPS_OUT'] = self.calc_bps(cur_data['CALC_COUNTER'], time_period)

                    elif (cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifHCInUcastPkts'] 
                        or cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifHCInMulticastPkts']
                        or cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifHCInBroadcastPkts']):
                        tmp_dict['PPS_IN'] = tmp_dict['PPS_IN'] + self.calc_pps(cur_data['CALC_COUNTER'], time_period)
                    elif (cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifHCOutUcastPkts'] 
                        or cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifHCOutMulticastPkts']
                        or cur_data['TRF_TYPE'] == cfg.SNMP_COLLECT_OIDS_DICT['ifHCOutBroadcastPkts']):
                        tmp_dict['PPS_OUT'] = tmp_dict['PPS_OUT'] + self.calc_pps(cur_data['CALC_COUNTER'], time_period)

                trf_dict[host_key] = tmp_dict

            except KeyError as e:
                print('Not found in previous snmp traffic')
                continue
            except Exception as e :
                print('Exception occur - ', e)
                continue

        return trf_dict.values()
        
    def calc_bps(self, bytes, second=60):
        bps = float(bytes) / float(second) * 8.0

        return int(bps)


    def calc_pps(self, packets, second=60):
        pps = float(packets) / float(second)

        return int(pps)


def main():
    print('START Sna_snmp_trf_collector Process!!!')
    mysql_exec = sqlExec(cfg.DB_HOST, cfg.DB_USER, cfg.DB_PASSWD, cfg.DB_NAME)

    if mysql_exec.conn_db is False:
        print("Can't connect database : check environmnet of database!!!")
        print('END Sna_snmp_trf_collector Process!!!')
        return
    
    trf_collector = SnaSnmpTrfCollector()
#---------------------------------------------------------------------
    targets = mysql_exec.select_equip_target_list()

    print(targets)

    for target in targets:
        try:
            prev_snmp_data = trf_collector.load(cfg.SNMP_DATA_FILENAME, target[0])
            snmp_data = trf_collector.get_snmp_traffic(target[0],
                    target[1],
                    cfg.SNMP_COLLECT_OIDS_DICT.values(),
                    cfg.SNMP_COUNT_OID
            )
            print("snmp_data = ")
            print(snmp_data)
            print

            if snmp_data is None :
                print("%s : collect traffic error" % target[0])
                continue

            save_snmp_data = trf_collector.make_save_data(target[0], snmp_data, prev_snmp_data)
              
            print("save_snmp_data = ")
            print(save_snmp_data)
            print
            trf_collector.save(cfg.SNMP_DATA_FILENAME, target[0], save_snmp_data) 
            
            save_trf_data = trf_collector.make_trf_data(save_snmp_data, prev_snmp_data)
            print(save_snmp_data)
            print('\n')
            mysql_exec.save_snmp_trf_list(save_trf_data)
            mysql_exec.commit()

            sna_errorEvent.main()#에러 파일 실행
        except Exception as e:
            print(e)
            continue

    threading.Timer(60, main).start()
            
#-------------------------------------------------------------------
    # prev_snmp_data = trf_collector.load(cfg.SNMP_DATA_FILENAME)
    # save_snmp_data = trf_collector.make_save_data(cfg.SNMP_TARGET, snmp_data, prev_snmp_data)

    

    # trf_collector.save(cfg.SNMP_DATA_FILENAME, save_snmp_data)    

    # save_trf_data = trf_collector.make_trf_data(save_snmp_data, prev_snmp_data)
    # mysql_exec.save_snmp_trf_list(save_trf_data)
    # mysql_exec.commit()

    # trf_collector.save(cfg.SNMP_DATA_FILENAME, save_snmp_data)

    # print('>> END : SNMP Collect Target - {0}'.format(cfg.SNMP_TARGET))


if __name__ == "__main__":
    main()
  
