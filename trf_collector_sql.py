# -*- coding: utf-8 -*-

import sys
import traceback
import base64

from Sna_mysql import SnaMySql



class TrfCollectorSql(SnaMySql) :
    def __init__(self,  host, user, watchword, db_name, port=3306, charset='utf-8', unicode=True):
        SnaMySql.__init__(self,  host, user, watchword, db_name, port, charset, unicode)
        self.sql_count = 0

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

    def select_snmp_traffic(self,cur_time):
        try:
            sql="""
                select eq_ip,if_index,in_traffic
                from snmp_traffic
                where tr_date = '"""+cur_time+"""'
                order by eq_ip,if_index
            """

            rows = self.exec_sql(sql)

            return rows

        except Exception as e:
            print("database is not exist")
            rows = '%s' % str(traceback.print_exc())
            print (rows)
            return rows

    def select_interface_speed(self):
        try:
            sql="""
                select eq_ip,if_index,speed
                from interface
                order by eq_ip,if_index
            """

            rows = self.exec_sql(sql)

            return rows

        except Exception as e:
            print("database is not exist")
            rows = '%s' % str(traceback.print_exc())
            print (rows)
            return rows

    def insert_day_traffic_list(self):
        try:
            sql = """
                INSERT INTO day_statistics
                (eq_ip ,if_index, st_date, 
                now_in_traffic, now_in_packet, now_out_traffic, now_out_packet, 
                max_in_traffic, max_in_packet, max_out_traffic, max_out_packet, 
                avg_in_traffic, avg_in_packet, avg_out_traffic, avg_out_packet)
                SELECT 
                eq_ip,if_index, FROM_UNIXTIME((UNIX_TIMESTAMP(DATE_ADD(DATE_FORMAT(tr_date , '%Y-%m-%d %H:%i:%S'), Interval 5 Minute)) -
				(UNIX_TIMESTAMP(date_add(DATE_FORMAT(tr_date, '%Y-%m-%d %H:%i:%S'), Interval 5 Minute)) % 300))) tr_date,
                ROUND(in_traffic) now_in_traffic,ROUND(in_packet) now_in_packet,
                ROUND(out_traffic) now_out_traffic,ROUND(out_packet) now_out_packet,
                ROUND(MAX(in_traffic),2) max_in_traffic,ROUND(MAX(in_packet),2) max_in_packet,
                ROUND(MAX(out_traffic),2) max_out_traffic,ROUND(MAX(out_packet),2) max_out_packet,
                ROUND(AVG(in_traffic),2) avg_in_traffic,ROUND(AVG(in_packet),2) avg_in_packet,
                ROUND(AVG(out_traffic),2) avg_out_traffic,ROUND(AVG(out_packet),2) avg_out_packet
                from snmp_traffic
                where (select max(st_date) from day_statistics) < tr_date or (select count(st_date) from day_statistics) = 0
                group by DATE(tr_date),FLOOR(HOUR(tr_date)),FLOOR(MINUTE(tr_date)/5) ,eq_ip ,if_index;      
            """
            rows = self.exec_sql(sql)

            return rows

        except Exception as e:
            print("database is not exist")
            rows = '%s' % str(traceback.print_exc())
            print (rows)
            return rows

    def insert_week_traffic_list(self):
        try:
            sql = """
                INSERT INTO week_statistics
                (eq_ip ,if_index, st_date, 
                now_in_traffic, now_in_packet, now_out_traffic, now_out_packet, 
                max_in_traffic, max_in_packet, max_out_traffic, max_out_packet, 
                avg_in_traffic, avg_in_packet, avg_out_traffic, avg_out_packet)
                SELECT 
                eq_ip,if_index, FROM_UNIXTIME((UNIX_TIMESTAMP(DATE_ADD(DATE_FORMAT(st_date , '%Y-%m-%d %H:%i:%S'), Interval 30 Minute)) -
				(UNIX_TIMESTAMP(date_add(DATE_FORMAT(st_date, '%Y-%m-%d %H:%i:%S'), Interval 30 Minute)) % 1800))) st_date,
                ROUND(now_in_traffic) now_in_traffic,ROUND(now_in_packet) now_in_packet,
                ROUND(now_out_traffic) now_out_packet,ROUND(now_out_packet) now_out_packet,
                ROUND(MAX(max_in_traffic),2) max_in_traffic,ROUND(MAX(max_in_packet),2) max_in_packet,
                ROUND(MAX(max_out_traffic),2) max_out_traffic,ROUND(MAX(max_out_packet),2) max_out_packet,
                ROUND(AVG(avg_in_traffic),2) avg_in_traffic,ROUND(AVG(avg_in_packet),2) avg_in_packet,
                ROUND(AVG(avg_out_traffic),2) avg_out_traffic,ROUND(AVG(avg_out_packet),2) avg_out_packet
                from day_statistics ds
                where (select max(st_date) from week_statistics) < ds.st_date or (select count(st_date) from week_statistics) = 0
                group by DATE(st_date),FLOOR(HOUR(st_date)),FLOOR(MINUTE(st_date)/30) ,eq_ip ,if_index;    
            """
            rows = self.exec_sql(sql)

            return rows

        except Exception as e:
            print("database is not exist")
            rows = '%s' % str(traceback.print_exc())
            print (rows)
            return rows

    def insert_month_traffic_list(self):
        try:
            sql = """
                INSERT INTO month_statistics
                (eq_ip ,if_index, st_date, 
                now_in_traffic, now_in_packet, now_out_traffic, now_out_packet, 
                max_in_traffic, max_in_packet, max_out_traffic, max_out_packet, 
                avg_in_traffic, avg_in_packet, avg_out_traffic, avg_out_packet)
                SELECT 
                eq_ip,if_index, FROM_UNIXTIME((UNIX_TIMESTAMP(DATE_ADD(DATE_FORMAT(st_date , '%Y-%m-%d %H:%i:%S'), Interval 1 Hour)) -
				(UNIX_TIMESTAMP(date_add(DATE_FORMAT(st_date, '%Y-%m-%d %H:%i:%S'), Interval 1 Hour)) % 3600))) st_date,
                ROUND(now_in_traffic) now_in_traffic,ROUND(now_in_packet) now_in_packet,
                ROUND(now_out_traffic) now_out_packet,ROUND(now_out_packet) now_out_packet,
                ROUND(MAX(max_in_traffic),2) max_in_traffic,ROUND(MAX(max_in_packet),2) max_in_packet,
                ROUND(MAX(max_out_traffic),2) max_out_traffic,ROUND(MAX(max_out_packet),2) max_out_packet,
                ROUND(AVG(avg_in_traffic),2) avg_in_traffic,ROUND(AVG(avg_in_packet),2) avg_in_packet,
                ROUND(AVG(avg_out_traffic),2) avg_out_traffic,ROUND(AVG(avg_out_packet),2) avg_out_packet
                from week_statistics ws
                where (select max(st_date) from month_statistics) < ws.st_date or (select count(st_date) from month_statistics) = 0
                group by DATE(st_date),FLOOR(HOUR(st_date)/1),MINUTE(st_date) ,eq_ip ,if_index;    
            """
            rows = self.exec_sql(sql)

            return rows

        except Exception as e:
            print("database is not exist")
            rows = '%s' % str(traceback.print_exc())
            print (rows)
            return rows

    def insert_year_traffic_list(self):
        try:
            sql = """
                INSERT INTO year_statistics
                (eq_ip ,if_index, st_date, 
                now_in_traffic, now_in_packet, now_out_traffic, now_out_packet, 
                max_in_traffic, max_in_packet, max_out_traffic, max_out_packet, 
                avg_in_traffic, avg_in_packet, avg_out_traffic, avg_out_packet)
                SELECT 
                eq_ip,if_index, FROM_UNIXTIME((UNIX_TIMESTAMP(DATE_ADD(DATE_FORMAT(st_date , '%Y-%m-%d %H:%i:%S'), Interval 2 Hour)) -
				(UNIX_TIMESTAMP(date_add(DATE_FORMAT(st_date, '%Y-%m-%d %H:%i:%S'), Interval 2 Hour)) % 7200))) st_date,
                ROUND(now_in_traffic) now_in_traffic,ROUND(now_in_packet) now_in_packet,
                ROUND(now_out_traffic) now_out_packet,ROUND(now_out_packet) now_out_packet,
                ROUND(MAX(max_in_traffic),2) max_in_traffic,ROUND(MAX(max_in_packet),2) max_in_packet,
                ROUND(MAX(max_out_traffic),2) max_out_traffic,ROUND(MAX(max_out_packet),2) max_out_packet,
                ROUND(AVG(avg_in_traffic),2) avg_in_traffic,ROUND(AVG(avg_in_packet),2) avg_in_packet,
                ROUND(AVG(avg_out_traffic),2) avg_out_traffic,ROUND(AVG(avg_out_packet),2) avg_out_packet
                from month_statistics ms
                where ((select max(st_date) from year_statistics) < ms.st_date) or (select count(st_date) from year_statistics) = 0
                group by DATE(st_date),FLOOR(HOUR(st_date)/2),MINUTE(st_date) ,eq_ip ,if_index;    
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
                insert into interface
                (eq_ip,if_index,name,mac_addr,
                alias,descr,speed,
                admin_status,oper_status)
                values
                (%(IP)s,%(IF_INDEX)s,%(IF_NAME)s,%(MAC_ADDR)s,
                %(IF_ALIAS)s,%(IF_DESCR)s, %(IF_SPEED)s,
                %(ADMIN_STATUS)s, %(OPER_STATUS)s)
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
                update interface
                set name=%(IF_NAME)s, 
                mac_addr=%(MAC_ADDR)s,
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

    def update_eq_list(self, snmp_eq_dict):
        row_count = -1
        try :
            sql = """
                update equipment
                set name=%(EQ_NAME)s, 
                descr=%(EQ_DESCR)s,
                location=%(EQ_LO)s
                where eq_ip = %(IP)s
            """
            print(sql)
            row_count = self.exec_many_Sna(sql, snmp_eq_dict)
            return row_count

        except Exception as e :
            print ("update_if() : Exception Occur -  ", e)
            msg = '%s' % str(traceback.print_exc())
            print (msg)

            return -1

    def update_snmp_error_list(self, error_dict):
        row_count = -1
        try :
            sql = """
                update event
                set type=%(TYPE)s, 
                grade=%(GRADE)s,
                ev_contents=%(EV_CON)s,
                occur=%(OCCUR)s,
                count=count+1
                where eq_ip = %(IP)s and if_index = %(INDEX)s
            """
            
            row_count = self.exec_many_Sna(sql, error_dict)
            print("updatecomplte")
            return row_count

        except Exception as e :
            print ("save_error_data() : Exception Occur -  ", e)
            msg = '%s' % str(traceback.print_exc())
            print (msg)
            return row_count
    
    def save_snmp_error_list(self, error_dict):
        row_count = -1
        try :
            # sql = """
            #     replace into event
            #     (type, grade, ev_contents, occur,
            #     count,id,eq_ip,if_index)
            #     values
            #     (%(TYPE)s,%(GRADE)s,%(EV_CON)s,%(OCCUR)s,
            #     %(COUNT)s,%(ID)s,%(IP)s, %(INDEX)s)
            # """

            # foo = error_dict['192.168.0.101-2'].get('EV_CON')
            # print("foo = ",foo)
            
            sql = """
                insert into event
                (type, grade, ev_contents, occur,
                count,id,eq_ip,if_index)
                values
                (%(TYPE)s,%(GRADE)s,%(EV_CON)s,%(OCCUR)s,
                %(COUNT)s,%(ID)s,%(IP)s, %(INDEX)s)
                on duplicate key update
                count = count+1,type = (%(TYPE)s),grade=%(GRADE)s,occur=(%(OCCUR)s),
                ev_contents=(%(EV_CON)s),id=(%(id)s)
            """

            #ev_contents='"""+ error_dict.get('EV_CON') +"""'

            row_count = self.exec_many_Sna(sql, error_dict)
            print("savecomplte")
            return row_count

        except Exception as e :
            print ("save_error_data() : Exception Occur -  ", e)
            msg = '%s' % str(traceback.print_exc())
            print (msg)
            return row_count

    def error_target_delete(self,ip,index):
        try:
            sql = """
                delete
                from event
                where eq_ip='"""+ip+"""' and if_index='"""+str(index)+"""'
                """

            rows = self.exec_sql(sql)

            return rows

        except Exception as e:
            print("database is not exist")
            rows = '%s' % str(traceback.print_exc())
            print (rows)
            return rows