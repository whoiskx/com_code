# -*- coding: utf-8 -*-
import pymysql


def uploads_mysql(config_mysql, sql, _tuple):
    db = pymysql.connect(**config_mysql)
    cursor = db.cursor()
    cursor.execute(sql, _tuple)
    db.commit()
    cursor.close()
    db.close()

# 微信旧库
import pymssql

MYSQL_HOST = '183.131.241.60'
MYSQL_PORT = 38019
MYSQL_USER = 'oofraBnimdA_gz'
MYSQL_PASSWORD = 'fo(25R@A!@8a823#@%'
MYSQL_DATABASE = 'Winxin'

config_mysql = {
    'server': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'database': MYSQL_DATABASE,
    'password': MYSQL_PASSWORD,
    'charset': 'utf8',
}
db = pymssql.connect(**config_mysql)
cursor = db.cursor()
