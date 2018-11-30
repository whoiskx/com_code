# from sqlalchemy import create_engine
#
# engine = create_engine()

# MYSQL_HOST = 'localhost'
# MYSQL_PORT = '3306'
# MYSQL_USER = ''
# MYSQL_PASSWORD = ''
# MYSQL_DATABASE = 'info_sct'

import pymysql
# Mysql settings
MYSQL_CLS = pymysql.Connection
MYSQL_ENCODING = 'utf8'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = None
MYSQL_DATABASE = 'mysql'
MYSQL_PARAMS = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'database': MYSQL_DATABASE,
    'charset': MYSQL_ENCODING,
}

db_fb = pymysql.connect(host='localhost',user='root',  port=3306,  database='db', db='db')
cursor = db_fb.cursor()
# sql = 'SELECT * FROM db'
# cursor.execute(sql)

# cursor.execute('SELECT VERSION()')
# data = cursor.fetchone()
# print('Database version:', data)

# create_sql = '''
#        CREATE TABLE fuck(
# id INT AUTO_INCREMENT PRIMARY KEY,
# username VARCHAR(255) UNIQUE ,
# nickname VARCHAR(255) NOT NULL ,
# birthday DATE
# )
#         '''
#
# cursor.execute(create_sql)
# db_fb.commit()

sql = 'SELECT * FROM db'
cursor.execute(sql)
for i in cursor:
    print(i)