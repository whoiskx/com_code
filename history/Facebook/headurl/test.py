import pymysql
#
# MYSQL_HOST = 'localhost'
# MYSQL_PORT = 3306
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = ''
# MYSQL_DATABASE = 'comm'
#
# config_mysql = {
#     'host': MYSQL_HOST,
#     'port': MYSQL_PORT,
#     'user': MYSQL_USER,
#     'db': MYSQL_DATABASE,
# }
#
# header_img = {
#     'host': MYSQL_HOST,
#     'port': MYSQL_PORT,
#     'user': MYSQL_USER,
#     'db': MYSQL_DATABASE,
# }
#
# db = pymysql.connect(**config_mysql)
# cursor = db.cursor()
# id, post_id,  header_url = 1,2, 3,
# cursor.execute('INSERT INTO header_url VALUES("%s", "%s", "%s", "%s")' % (id, post_id, 4, header_url))
# db.commit()



MYSQL_HOST = '47.52.190.138'
MYSQL_PORT = 8002
MYSQL_USER = 'yunrun'
MYSQL_PASSWORD = 'Yunrun2015!@#'
MYSQL_DATABASE = 'weibotask'

# MYSQL_HOST = '121.28.84.254'
# MYSQL_PORT = 7101
# MYSQL_USER = 'yunrun'
# MYSQL_PASSWORD = 'Yunrun2015!@#'
#
# MYSQL_HOST = '219.143.144.227'
# MYSQL_PORT = 38112
# MYSQL_USER = 'user_taizhou'
# MYSQL_PASSWORD = 'taizhou123'
# MYSQL_DATABASE = 'weibotask'

config_mysql = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'passwd': MYSQL_PASSWORD
    # 'db': MYSQL_DATABASE,
}

db = pymysql.connect(**config_mysql)
# cursor = db.cursor()
# cursor.execute('select * FROM imagefail')
# data = cursor.fetchmany(10)
# for i in data:
#     print(i)
