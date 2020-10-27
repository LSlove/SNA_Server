# -*- coding: utf-8 -*-

"""
Created    : 2019. 11. 26
Programmer : bugslayer
Purpose    : SNMP 수집 프로세스의 DB Query 처리를 위한 라이브러리

"""

import sys
import traceback
import base64

from dml_mysql import DmlMySql
#from dml_base.dml_util import dml_util as Util

class TrfCollectorSql(DmlMySql) :
    def __init__(self,  host, user, watchword, db_name, port=3306, charset='utf-8', unicode=True):
        DmlMySql.__init__(self,  host, user, watchword, db_name, port, charset, unicode)

    def select_equip_target_list(self):
        try:
            sql = """
                select eq_ip, read_community, snmp_port, snmp_version 
                from equipment_snmpsetting           
            """
            rows = self.exec_sql(sql)

            return rows

        except Exception as e:
            print("database is not exist")
            rows = '%s' % str(traceback.print_exc())
            print (rows)
            return rows


    def save_snmp_trf_list(self, snmp_trf_dict):
        row_count = -1
        try :
            sql = """
                insert into snmp_traffic
                (eq_ip,if_index, tr_date, 
                in_traffic,in_packet,out_traffic,out_packet)
                values
                (%(IP)s,%(SNMP_INDEX)s,%(TIMESTAMP)s,
                 %(BPS_IN)s, %(PPS_IN)s, %(BPS_OUT)s, %(PPS_OUT)s)
            """

            row_count = self.exec_many_dml(sql, snmp_trf_dict)
            return row_count

        except Exception as e :
            print ("save_snmp_trf() : Exception Occur -  ", e)
            msg = '%s' % str(traceback.print_exc())
            print (msg)
            return row_count
