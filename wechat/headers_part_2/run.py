# -*- coding: utf-8 -*-
import os
import pymssql

from config import get_mysql_old
from utils import log, log2
from headers import *


def check_image(account_info):
    # Images/50000/50000350.jpg
    account_id = str(account_info[0])
    user_file_dir = r'D:\WXSchedule\Images'
    num = int(account_id) // 1000
    IMAGE_DIR = os.path.join(user_file_dir, str(num))
    path = os.path.join(IMAGE_DIR, account_id + '.jpg')
    log(path)
    if os.path.exists(path):
        log2(list(account_info), '头像已存在')
    else:
        save_images(account_info)


def save_images(account_info):
    name = account_info[2]
    # mysql_config = get_mysql_old()
    # db = pymssql.connect(**mysql_config)
    # cursor = db.cursor()
    # sql_select = """
    #         select id from wxaccount where account=%s
    # """
    # cursor.execute(sql_select, (name,))
    # result = cursor.fetchall()
    # log(result)
    # if len(result) > 0:
    # info = result[0]
    account_id = account_info[0]
    account.name = name
    account.account = account_id
    result = account.run()
    if result == '完成':
        log2(list(account_info), '头像上传成功')
    else:
        log2(list(account_info), '搜狗匹配不到该账号')
    # else:
    #     return '数据库找不到该账号'
    # return result


def main():
    mysql_config = get_mysql_old()
    db = pymssql.connect(**mysql_config)
    cursor = db.cursor()
    sql_select = """
            select id, name, account from wxaccount where id >65000000 and id < 67000000 order by id asc  
    """
    cursor.execute(sql_select)
    result = cursor.fetchall()
    for r in result:
        print(r)
        check_image(r)
    # print(list(result))


if __name__ == '__main__':
    main()
