import time
import pymysql
from setting import urun,  hash_md5
import datetime

MYSQL_HOST = '47.52.190.138'

MYSQL_PORT = 8002
MYSQL_USER = 'yunrun'
MYSQL_PASSWORD = 'Yunrun2015!@#'
MYSQL_DATABASE = 'weibotask'

config_mysql = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'db': MYSQL_DATABASE,
    'passwd': MYSQL_PASSWORD,
    'charset': 'utf8',

}

db = pymysql.connect(**config_mysql)
cursor = db.cursor()


datas = urun['fb_bukong'].find()
flag = ''
try:
    for index, d in enumerate(datas):
        print(index, d)
        if index == 62:
            name = d.get('name')
            url = d.get('url')
            Addon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # remark = name
            cursor.execute(
                "INSERT INTO task_public(ID, site, name, type, url, remark, Sex, language, Country, Addon, Enabled, Oversea, IsPublic) VALUES  (  %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s)", (
                    hash_md5(name+url[-9:]), 3, name, 1, url, name, 0, 0, 0, Addon,  1, 0, 1))
            db.commit()

        #
        # if index > 6:
        #     break
except Exception as e:
    print(e)
    flag = 's'
# if flag != 's':
#     db.commit()
