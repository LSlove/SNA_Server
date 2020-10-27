# -*- coding: utf-8 -*-

#import MySQLdb
import pymysql
import traceback

class SnaMySql(object):
    def __init__(self, host, user, passwd, db_name, port=3306, charset='utf-8', unicode=True):
        self.host 	= host
        self.user 	= user
        self.passwd = passwd
        self.db_name= db_name
        self.port	= port
        self.db     = None

        self.conn_db = self._connect_db(host, user, passwd, db_name, int(port), charset=charset, use_unicode=unicode)


    def __del__(self):
        try :
            self.close_db()
        except Exception as e :
            print ("SnaMySql:__del__ : Exception Occur - ", e)
            return


    def _connect_db(self,  host, user, passwd, db_name, port=3306, charset='utf-8', use_unicode=True):
        try:

            # self.db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name, port=port, charset=charset, use_unicode=use_unicode)
            self.db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name, port=port)

        except pymysql.Error as e:
            print ("_connectDB() - DB Connection Fail : ", e)
            traceback.print_exc()
            return False
        except Exception as e :
            print ("SnaMySql :_connectDB() :  Exception Occur - ", e)
            traceback.print_exc()
            return False

        return True


    def close_db(self):
        try :
            if self.conn_db:
                self.db.close()
                self.db = None
        except Exception as e :
            print ("SnaMySql:close_db() : Exception Occur - ", e)
            print ("DB = ", self.db_name)
            return


    def open_cursor(self) :
        try :
            if self.conn_db :
                return self.db.cursor()
        except Exception as e :
            print ("SnaMySql:open_cursor() : Exception Occur - ", e)
            return


    def close_cursor(self, cursor) :
        try :
            cursor.close()
        except Exception as e :
            print ("SnaMySql:close_cursor() : Exception Occur - ", e)
            return


    def commit(self) :
        try :
            self.db.commit()
        except Exception as e :
            print ("SnaMySql:commit() : Exception Occur - ", e)
            return


    def rollback(self) :
        try :
            self.db.rollback()
        except Exception as e :
            print ("SnaMySql:rollback() : Exception Occur - ", e)
            return


    def exec_sql(self, sql) :
        try:
            cursor = self.open_cursor()
			# cursor.arraysize = cursor.bindarraysize = 100
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.close_cursor(cursor)

            return rows

        except Exception as e :
            print ("SnaMySql : exec_sql() : Exception Occur - ", e)
            self.close_cursor(cursor)
            return False


    def exec_Sna(self, sql) :
        try:

            row_count = -1

            cursor = self.open_cursor()
            cursor.execute(sql)

            row_count = cursor.rowcount
            self.close_cursor(cursor)

            return row_count

        except Exception as e :
            print ("SnaMySql : exec_Sna_sql() : Exception Occur - ", e)
            self.close_cursor(cursor)
            return False


    def exec_var(self, sql, *arg_list) :
        try:
            cursor = self.open_cursor()
            cursor.execute(sql, arg_list)
            rows = cursor.fetchall()
            self.close_cursor(cursor)

            return rows

        except Exception as e :
            print ("SnaMySql : exec_sql_var() : Exception Occur - ", e)
            self.close_cursor(cursor)
            return False


    def exec_Sna_var(self, sql, *arg_list) :
        try:
            row_count = -1

            cursor = self.open_cursor()
            cursor.execute(sql, arg_list)

            row_count = cursor.rowcount

            self.close_cursor(cursor)

            return row_count
        except Exception as e :
            print ("SnaMySql : exec_Sna_sql_var() : Exception Occur - ", e)
            self.close_cursor(cursor)
            return False


    def exec_many_Sna(self, sql, rows) :
        try:
            row_count = -1

            cursor = self.open_cursor()
            cursor.executemany(sql, rows)

            row_count = cursor.rowcount
            self.close_cursor(cursor)

            return row_count

        except Exception as e :
            print ("SnaMySql : exec_many_Sna_sql() : Exception Occur - ", e)
            print ("Query = ", sql)
            print ("Error Data = ", rows)
            self.close_cursor(cursor)
            return False


    # 유틸성 함수 모음 - 데이터 삭제, 테이블 이름 변경, 테이블 드랍등.
    def truncate_table(self, tbl_name) :

        try :
            sql = "TRUNCATE TABLE %s " % (tbl_name)
            print ("SQL = %s " % sql)
            ret = self.exec_Sna_sql(sql)

            return ret
        except Exception as e :
            print ("truncate_table() : Exception - ", e)
            return None


    def rename_table(self, from_name, to_name) :

        try :
            sql = """
                    ALTER TABLE %s
                    RENAME TO %s
                """ % (from_name, to_name)
            print ("SQL = ", sql)

            self.exec_Sna_sql(sql)

        except Exception as e :
            print ("rename_table() : Exception Occur - ", e)
            return None


    def drop_table(self, tbl_name) :
        try :

            sql = "DROP TABLE %s " % (tbl_name)
            print ("SQL = %s " % sql)
            ret = self.exec_Sna_sql(sql)

            return ret
        except Exception as e :
            print ("drop_table() : Exception - ", e)
            return None


    def drop_index(self, idx_name) :
        try :
            sql = "DROP INDEX %s " % (idx_name)
            print ("SQL = %s " % sql)
            ret = self.exec_Sna_sql(sql)

            return ret
        except Exception as e :
            print ("dropIndex() : Exception - ", e)
            return None


    def change_table_key(self, tbl_name, enable=True):
        try :

            if enable :
                sql = "ALTER TABLE %s ENABLE KEYS " % (tbl_name)
            else :
                sql = "ALTER TABLE %s DISABLE KEYS " % (tbl_name)

            print ("SQL = %s " % sql)
            ret = self.exec_Sna_sql(sql)

            return ret
        except Exception as e :
            print ("change_table_key() : Exception - ", e)
            return None


    def change_myisam_check_state(self, enable = True):
        try :
            sql_commit_exec = None

            if enable is False:
                sql_commit 		= "SET autocommit = 0 "
                sql_unique 		= "SET unique_checks = 0 "
                sql_fk 			= "SET foreign_key_checks = 0 "
                sql_session 	= "SET SESSION tx_isolation='READ-UNCOMMITTED' "
            else :
                sql_commit 		= "SET autocommit = 1 "
                sql_commit_exec = "COMMIT "
                sql_unique 		= "SET unique_checks = 1 "
                sql_fk 			= "SET foreign_key_checks = 1 "
                sql_session 	= "SET SESSION tx_isolation='READ-REPEATABLE' "

            ret1 = self.exec_Sna_sql(sql_commit)
            ret2 = self.exec_Sna_sql(sql_unique)
            ret3 = self.exec_Sna_sql(sql_fk)
            if sql_commit_exec is not None :
                ret4 = self.exec_Sna_sql(sql_commit_exec)

            ret5 = self.exec_Sna_sql(sql_session)

            return True
        except Exception as e :
            print ("change_myisam_check_state() : Exception - ", e)
            return None