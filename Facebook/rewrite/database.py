from utils import db_mysql
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cursor = db_mysql.cursor()

mysql_find_all = """
        SELECT * FROM task_2
"""
cursor.execute(mysql_find_all)

records = cursor.fetchmany(200)

# print(records)
count = 0
if records:
    for record in records:
        url = record[4]
        if 'facebook' in url:
            import redis  # 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.lpush('fb_home_url', url)
            count += 1
            print('添加了{}条 :{}'.format(count, url))
