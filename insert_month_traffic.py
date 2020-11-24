from trf_collector_sql import TrfCollectorSql as sqlExec
import SNA_config as cfg

def main():
    mysql_exec = sqlExec(cfg.DB_HOST, cfg.DB_USER, cfg.DB_PASSWD, cfg.DB_NAME)
    if mysql_exec.conn_db is False:
        print("Can't connect month list database")
        return
    else:
        mysql_exec.insert_month_traffic_list()
        mysql_exec.commit()
        return

if __name__ == "__main__":
    main()