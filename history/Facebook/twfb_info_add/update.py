# -*- coding: utf-8 -*-

def mysql_localhost():
    # MYSQL_HOST = 'localhost'
    # MYSQL_PORT = 3306
    # MYSQL_USER = 'root'
    # MYSQL_PASSWORD = ''
    # MYSQL_DATABASE = 'comm'
    MYSQL_HOST = '120.78.237.213'
    MYSQL_PORT = 8002
    MYSQL_USER = 'yunrun'
    MYSQL_PASSWORD = 'Yunrun2016!@#'
    MYSQL_DATABASE = 'urun_statistic'

    config_mysql = {
        'host': MYSQL_HOST,
        'port': MYSQL_PORT,
        'user': MYSQL_USER,
        'db': MYSQL_DATABASE,
        'passwd': MYSQL_PASSWORD,
        'charset': 'utf8',
    }
    return config_mysql

import pymysql
mysql_params = mysql_localhost()
db = pymysql.connect(**mysql_params)
cursor = db.cursor()
cursor.execute("SELECT uid,Description FROM `twfb_copy` where Url like '%facebook%';")

date_all = list(cursor.fetchmany(100))
print(date_all)
# for date in date_all:
#     try:
#         sql = """
#         update twfb_copy set Description=%s where uid=%s
#         """
#         cursor.execute(sql, date)
#         db.commit()
#     except Exception as e:
#         print('error', date)
#         db.rollback()

