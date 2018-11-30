# import time
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pymysql
# from setting import test, log
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
# cursor_save = db.cursor()
#
# cursor.execute('select * FROM imagefail')
# count = 0
# urls = cursor.fetchmany(4707)
# # urls = cursor.fetchmany(89)
# while True:
#     # if count < 2:
#     #     count += 1
#     #     continue
#     urls = cursor.fetchmany(1000)
#     prefs = {
#         'profile.default_content_setting_values': {
#             'images': 2,
#             'javascript': 2,
#         }
#     }
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option('prefs', prefs)
#     driver = webdriver.Chrome(chrome_options=options)
#     # driver.set_page_load_timeout(1)
#     # driver.set_script_timeout(1)
#     time.sleep(5)
#     for index, url_tuple in enumerate(urls):
#         numb, post_id, _ = url_tuple
#         header_url_person = ''
#         header_url_group = ''
#         url = 'https://www.facebook.com/' + post_id
#         driver.get(url)
#         time.sleep(1)
#         log(index, url)


from selenium    import webdriver

d = webdriver.Chrome()
d.get('https://www.facebook.com/directory/people/')
print('end')