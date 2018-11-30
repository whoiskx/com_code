# -*- coding: utf-8 -*-
import pymssql
from config import *

print = logger.info


class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        try:
            conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db,
                                   charset='cp936')
            return conn
        except Exception as e:
            print('pymssql：连接数据库失败..{}'.format(e))
            logger.error('pymssql：连接数据库失败..{}'.format(e))
            return None

    # 判断是否有该微信号
    def get_account(self, account):
        result = []
        conn = self.__GetConnect()
        if conn:
            cur = conn.cursor()
            try:
                sql = """SELECT * FROM WXAccount WHERE Account = '{}'""".format(account)
                cur.execute(sql)
                result = cur.fetchall()
            except Exception as e:
                print('sql server查询出错：{}...{}'.format(account, e))
                logger.error('sql server查询出错：{}...{}'.format(account, e))
            finally:
                cur.close()
                conn.close()

        return result

    # 添加新的公众号
    def add_account(self, name, account, url, collectiontime, biz):
        conn = self.__GetConnect()
        if conn:
            cur = conn.cursor()
            sql = """INSERT INTO WXAccount(Name,Account,Url,CollectionTime,Biz)
                     VALUES ('{}','{}','{}','{}','{}')""".format(name, account, url, collectiontime, biz)
            try:
                # 执行sql语句
                cur.execute(sql)
                # 提交到数据库执行
                conn.commit()
                print('增源：插入成功：{}'.format(account))
            except Exception as e:
                print('增源：插入失败：{}...{}'.format(account, e))
                logger.error('增源：插入失败：{}...{}'.format(account, e))
                # 如果发生错误则回滚
                conn.rollback()
            finally:
                cur.close()
                conn.close()


my_sqlserver = MSSQL(SQL_SERVER_HOST, SQL_SERVER_USER, SQL_SERVER_PWD, SQL_SERVER_DB)
