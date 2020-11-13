# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
import traceback

from sna_snmp import SnaSnmp as snmp
from trf_collector_sql import TrfCollectorSql as sqlExec
import SNA_config as cfg

import threading
import time

class ErrorCollector(object):
    def __init__(self):
        self.snmp = snmp()

    def errorSwitch(self,max,cur):
        grade = ''
        if((max*0.85)<cur):
            grade = 'Critical'
        elif((max*0.7)<cur):
            grade = 'Major'
        elif((max*0.45)<cur):
            grade = 'Minor'
        elif((max*0.34)<cur):
            grade = 'Warning'
        else:
            grade='Normal'
        
        return grade

    def save_error_data(self,eq_ip,if_index,grade,cur_now):
        tmp_dict = {}
        err_dict={}
        key = ('{0}-{1}'.format(eq_ip, if_index))
        try:
            print("start")
            tmp_dict['TYPE'] = 'traffic'
            tmp_dict['GRADE'] = grade
            tmp_dict['EV_CON'] = 'traffic_over'
            tmp_dict['OCCUR'] = cur_now
            tmp_dict['COUNT'] = 1
            tmp_dict['IP'] = eq_ip
            tmp_dict['INDEX'] = if_index

            err_dict[key] = tmp_dict

        except KeyError as e:
            print('Not found in Error Data')
        except Exception as e :
            print('Exception occur - ', e)

        err_dict[key] = tmp_dict

        print(err_dict)

        return err_dict.values()
         
def main():
    print('START Sna_Error_collector Process!!!')
    mysql_exec = sqlExec(cfg.DB_HOST, cfg.DB_USER, cfg.DB_PASSWD, cfg.DB_NAME)

    if mysql_exec.conn_db is False:
        print("Can't connect database : check environmnet of database!!!")
        print('END Error_collector Process!!!')
        return

#---------------------------------------------------------------------
    #datetime.fromtimestamp(int(cur_timestamp - (cur_timestamp % cfg.TRF_PERIOD)))
    now = time.time()
    cur_now =  datetime.fromtimestamp(int(now-(now%60)))

    try:
        snmptraffic = mysql_exec.select_snmp_traffic(str(cur_now))
        print("snmp_traffic = ",snmptraffic)
        if_speed =  mysql_exec.select_interface_speed()
        print("if_speed = ", if_speed)
        errorEvent = ErrorCollector()

        for targets in range(len(if_speed)):
            cheak_count = 0
            for target in range(len(if_speed[targets])):
                if(target == 0 or target == 1):
                    if(if_speed[targets][target] == snmptraffic[targets][target]):
                        cheak_count += 1
                elif(cheak_count == 2):
                    max_speed = int(if_speed[targets][target])/10
                    cur_speed = int(snmptraffic[targets][target])
                    error_Result = errorEvent.errorSwitch(max_speed,cur_speed)

                    if(error_Result!='Normal'):
                        save_error = errorEvent.save_error_data(snmptraffic[targets][0],snmptraffic[targets][1],error_Result,cur_now)
                        print("save error = ",save_error)
                        mysql_exec.save_snmp_error_list(save_error)
                        mysql_exec.commit()
                        print("End ErrorData")
                else:
                    print("check Interface DB",if_speed[0][0])
    except Exception as e:
        print(e)

                    

if __name__ == "__main__":
    main()