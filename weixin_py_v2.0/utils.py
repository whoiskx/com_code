# -*- coding: utf-8 -*-
import time

import pymysql
import pymssql


def uploads_mysql(config_mysql, sql, _tuple):
    db = pymysql.connect(**config_mysql)
    cursor = db.cursor()
    cursor.execute(sql, _tuple)
    db.commit()
    cursor.close()
    db.close()


# 微信旧库
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
with open('ids.txt', 'r', encoding='utf-8') as f:
    name_all = f.read()
id_list = name_all.split("\n")
print(id_list)


def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)