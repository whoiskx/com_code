# -*- coding: utf-8 -*-
import pymssql
from SougouWeixin.config import *


class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset='utf8')
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    # 判断是否有该微信号
    def get_account(self, account):
        cur = self.__GetConnect()
        sql = """SELECT * FROM WXAccount_copy_copy WHERE Account = '{}'""".format(account)
        cur.execute(sql)
        result = cur.fetchall()
        self.conn.close()
        return result

    # 添加新的公众号
    def add_account(self, name, account, url, collectiontime, biz):
        cur = self.__GetConnect()

        sql = """INSERT INTO WXAccount_copy_copy(Name,Account,Url,CollectionTime,Biz)
                 VALUES ('{}','{}','{}','{}','{}')""".format(name, account, url, collectiontime, biz)
        try:
            # 执行sql语句
            cur.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
            print('增源：插入成功：{}'.format(account))
        except Exception as e:
            print('增源：插入失败：{}'.format(account))
            print(e)
            # 如果发生错误则回滚
            self.conn.rollback()
        self.conn.close()


my_sqlserver = MSSQL(SQL_SERVER_HOST, SQL_SERVER_USER, SQL_SERVER_PWD, SQL_SERVER_DB)
