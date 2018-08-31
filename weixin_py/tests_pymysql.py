# # -*- coding: UTF-8 -*-
# import csv
# import sys, os
# import pymysql
#
#
# def read_csv(filename):
#     '''
#     读取csv文件
#     '''
#     data = []
#     with open(filename) as f:
#         f_csv = csv.reader(f)
#         headers = next(f_csv)
#         # 数据格式[1111,22222,1111,1111,.....]
#         for row in f_csv:
#             # Process row
#             field1 = row[0]
#             data.append(row)
#         print
#         headers
#     return data
#
#
# def load_data():
#     '''
#     插入数据库
#     '''
#     filename = sys.argv[1]
#     try:
#         # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
#         conn = pymysql.connect(host='192.168.1.161', user='naliworld', passwd='password!', db='search', port=3306,
#                                charset='utf8')
#         cur = conn.cursor()  # 获取一个游标
#         data = read_csv(filename)
#         for row in data:
#             # Process row
#             field1 = row[0]
#             sql = '''insert into search.tb_text_uid_list(appId,type,uid,creator,createTime) values({},{},{},{},{}) '''.format(
#                 3, 1, field1, '\'admin\'', '\'2018-08-14 13:44:09\'')
#             print
#             sql
#             cur.execute(sql)
#         cur.close()  # 关闭游标
#         conn.commit()
#         conn.close()  # 释放数据库资源
#     except  Exception as e:
#         print(e)
#
#
# def get_sql():
#     '''
#     插入数据库生成插入sql
#     '''
#     sql_list = []
#     filename = sys.argv[1]
#     data = read_csv(filename)
#     for row in data:
#         # Process row
#         field1 = row[0]
#         sql = '''replace into search.tb_text_uid_list(appId,type,uid,creator,createTime) values({},{},{},{},{}) '''.format(
#             3, 1, field1, '\'admin\'', '\'2018-08-14 13:44:09\'')
#         sql_list.append(sql)
#     file_object = open('sql.txt', 'w')
#     file_object.writelines([line + ';\n' for line in sql_list])
#     file_object.close()
#
#
# if __name__ == "__main__":
#     get_sql()
#
#
#
#
#
#
#
import pymssql
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

# 问题：每次请求连接还是一直连接
db = pymssql.connect(**config_mysql)
cursor = db.cursor()
cursor.execute("SELECT * FROM test")
cursor.execute("INSERT INTO test(name, age) VALUES ({}, {})".format ('2321', '444'))
db.commit()
