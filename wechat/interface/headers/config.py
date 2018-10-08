# -*- coding: utf-8 -*-
import time


def mysql_tag_code():
    # 接口 site_id -> tag_code
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


# 微信旧库
def get_mysql_old():
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
    return config_mysql


# 新调度库
def get_mysql_new():
    """save data"""
    MYSQL_HOST = '121.28.84.254'
    MYSQL_PORT = 7101
    MYSQL_USER = 'yunrun'
    MYSQL_PASSWORD = 'YunRun2018!@#'
    MYSQL_DATABASE = 'test'

    config_mysql = {
        'host': MYSQL_HOST,
        'port': MYSQL_PORT,
        'user': MYSQL_USER,
        'passwd': MYSQL_PASSWORD,
        'db': MYSQL_DATABASE,
        'charset': 'utf8'
    }
    return config_mysql



