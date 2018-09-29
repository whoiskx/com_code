import pymysql

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

db = pymysql.connect(**config_mysql)
cursor = db.cursor()
# cursor.execute("UPDATE account SET  LogoUrl='Images/0/0.jpg' WHERE  LogoUrl=''")
# db.commit()
# itmes = cursor.fetchmany(10)
# for i in itmes:
#     print(i)
cursor.execute("select LogoUrl, Account from  account")
itmes = cursor.fetchall()
import requests

for index, i in enumerate(itmes):
    print(i)
    url = 'http://60.190.238.188:38016/{}'.format(i[0])

    r = requests.get(url)
    print(r.status_code)
    if r.status_code >= 300:
        cursor.execute("UPDATE account SET  LogoUrl='Images/0/0.jpg' WHERE  account=%s", (i[1],))
        print(index, i[0], )
        print('=====================')
    db.commit()

print(1)