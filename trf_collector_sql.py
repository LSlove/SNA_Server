# -*- coding: utf-8 -*-

import sys
import traceback
import base64

from Sna_mysql import SnaMySql

class TrfCollectorSql(SnaMySql) :
    def __init__(self,  host, user, watchword, db_name, port=3306, charset='utf-8', unicode=True):
        SnaMySql.__init__(self,  host, user, watchword, db_name, port, charset, unicode)

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

            row_count = self.exec_many_Sna(sql, snmp_trf_dict)
            return row_count

        except Exception as e :
            print ("save_snmp_trf() : Exception Occur -  ", e)
            msg = '%s' % str(traceback.print_exc())
            print (msg)
            return row_count

    def save_if_list(self, snmp_if_dict):
        row_count = -1
        try :
            # sql = """
            #     insert into Interface
            #     (eq_ip,if_index,name, 
            #     alias,descr,speed,admin_status,oper_status)
            #     values
            #     (%(IP)s,%(IF_INDEX)s,%(IF_NAME)s,%(IF_ALIAS)s,
            #     %(IF_DESCR)s, %(IF_SPEED)s, %(ADMIN_STATUS)s, %(OPER_STATUS)s)
            #     on duplicate key update
            #     name=%(IF_NAME)s, alias=%(IF_ALIAS)s,
            #     descr=%(IF_DESCR)s,speed=%(IF_SPEED)s,
            #     admin_status=%(ADMIN_STATUS)s,oper_status=%(OPER_STATUS)s
            # """

            sql = """
                insert into Interface
                (eq_ip,if_index,name, 
                alias,descr,speed,admin_status,oper_status)
                values
                (%(IP)s,%(IF_INDEX)s,%(IF_NAME)s,%(IF_ALIAS)s,
                %(IF_DESCR)s, %(IF_SPEED)s, %(ADMIN_STATUS)s, %(OPER_STATUS)s)
            """
            row_count = self.exec_many_Sna(sql, snmp_if_dict)
            return row_count

        except Exception as e :
            print ("save_if() : Exception Occur -  ", e)
            msg = '%s' % str(traceback.print_exc())
            print (msg)

            return -1
        
    def save_equip_list(self, snmp_if_dict):
        row_count = -1
        try :
            sql = """
                insert into equipment
                (eq_ip,name,vendor, 
                model,descr,location,manage,team)
                values
                (%(E_IP)s,%(E_NAME)s,NULL,NULL,
                %(E_DESCR)s, %(E_LOCATION)s,NULL,NULL)
            """
            row_count = self.exec_many_Sna(sql, snmp_if_dict)
            return row_count

        except Exception as e :
            print ("save_if() : Exception Occur -  ", e)
            msg = '%s' % str(traceback.print_exc())
            print (msg)

            return -1


    def update_if_list(self, snmp_if_dict):
        row_count = -1
        try :
            sql = """
                update Interface
                set name=%(IF_NAME)s, 
                alias=%(IF_ALIAS)s,
                descr=%(IF_DESCR)s,
                speed=%(IF_SPEED)s,
                admin_status=%(ADMIN_STATUS)s,
                oper_status=%(OPER_STATUS)s
                where eq_ip = %(IP)s and if_index = %(IF_INDEX)s
            """
            print(sql)
            row_count = self.exec_many_Sna(sql, snmp_if_dict)
            return row_count

        except Exception as e :
            print ("update_if() : Exception Occur -  ", e)
            msg = '%s' % str(traceback.print_exc())
            print (msg)

            return -1
    