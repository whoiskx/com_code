# -*- coding: utf-8 -*-
import pymongo
import time

import pymysql


# 新调度库
def get_mysql_new():
    """save data"""
    mysql_host = '121.28.84.254'
    mysql_port = 7101
    mysql_user = 'yunrun'
    mysql_password = 'YunRun2018!@#'
    mysql_database = 'info_src'

    config_mysql = {
        'host': mysql_host,
        'port': mysql_port,
        'user': mysql_user,
        'passwd': mysql_password,
        'db': mysql_database,
        'charset': 'utf8',
        'connect_timeout': 15,
    }
    return config_mysql


def get_account_form_weixin():
    _db = pymysql.connect(**get_mysql_new())
    _cursor = _db.cursor()
    sql = """
        SELECT * FROM weixin WHERE pause=0 LIMIT 7000;
    """
    _cursor.execute(sql)
    data = _cursor.fetchall()
    account_list = []
    for account_info in data:
        account_list.append(account_info[2])
    return account_list


# 搜狗验证码识别url
GETCAPTCHA_URL = 'http://124.239.144.164:7101/GetCaptcha'
# 主：河北164：23317
GETCAPTCHA_URL_MAIN = 'http://124.239.144.164:7101/GetCaptcha'
# 备用：广外204：38012
GETCAPTCHA_URL_BACKUP = 'http://183.238.76.204:38015/GetCaptcha'

# 补采
# ['bdb1937', 'dgshs2018', 'pd0351', 'guyuanxuanjiang', 'dgrb789']
ADD_COLLECTION = []  # get_account_form_weixin()
# 直接从数据库拿账号
GET_ACCOUNT_FROM_MYSQL = False
# 判重
JUDEG = True
# 使用代理
USE_PROXY = True


def mysql_tag_code():
    # 接口 site_id -> tag_code
    mysql_host = '120.78.237.213'
    mysql_port = 8002
    mysql_user = 'yunrun'
    mysql_password = 'Yunrun2016!@#'
    mysql_database = 'urun_statistic'

    config_mysql = {
        'host': mysql_host,
        'port': mysql_port,
        'user': mysql_user,
        'db': mysql_database,
        'passwd': mysql_password,
        'charset': 'utf8',
    }
    return config_mysql


# 微信旧库
def get_mysql_old():
    mysql_host = '183.131.241.60'
    mysql_port = 38019
    mysql_user = 'oofraBnimdA_gz'
    mysql_password = 'fo(25R@A!@8a823#@%'
    mysql_database = 'Winxin'

    config_mysql = {
        'server': mysql_host,
        'port': mysql_port,
        'user': mysql_user,
        'database': mysql_database,
        'password': mysql_password,
        'charset': 'utf8',
        'connect_timeout': 10
    }
    return config_mysql


def localhost_mysql():
    mysql_host = 'localhost'
    mysql_port = 3306
    mysql_user = 'root'
    mysql_database = 'comm'

    config_mysql = {
        'host': mysql_host,
        'port': mysql_port,
        'user': mysql_user,
        # 'passwd': mysql_password,
        'db': mysql_database,
        'charset': 'utf8',
        'connect_timeout': 10,
    }
    return config_mysql


def mongo_conn():
    conn = pymongo.MongoClient('120.78.237.213', 27017)
    _db = conn.account_count
    return _db


if __name__ == '__main__':
    # config_sql = localhost_mysql()
    # db = pymysql.connect(**config_sql)
    # cursor = db.cursor()
    # # cursor.execute(sql, _tuple)
    # # db.commit()
    # cursor.close()
    # db.close()
    print(get_account_form_weixin())
