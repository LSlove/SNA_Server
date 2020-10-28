# -*- coding: utf-8 -*-

import collector_config as cfg
import pymysql


def main():
    conn=pymysql.connect(host=cfg.DB_host,user=cfg.DB_user,password=cfg.DB_password,db=cfg.DB_db,charset='utf8')
    curs=conn.cursor()
    sql='insert into equip_performance(eq_ip,record_date,cpu_use,memory_use,disk_use) values (NULL,%s,%s,%s,%s)'
    #curs.execute(sql,(cfg.ip,cfg.nowDatetime,cfg.cpu,cfg.memory,cfg.disk))
    curs.execute(sql,(cfg.nowDatetime,cfg.cpu,cfg.memory,cfg.disk))

    sql='select * from equip_performance'
    curs.execute(sql)   
    rows=curs.fetchall()
    print(rows)
    conn.commit()
    conn.close()
    
    
        
if __name__=="__main__":
    main()