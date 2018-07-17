import time
from random import randint

from selenium import webdriver
from selenium.webdriver.common.action_chains import *
import pymongo

driver = webdriver.Chrome()
url = 'http://www.qq.com/'
driver.get(url)
time.sleep(5)

login = driver.find_element_by_class_name('login')
login.click()
time.sleep(3)
driver.switch_to.frame('ui_ptlogin')
time.sleep(2)

link = driver.find_element_by_id('switcher_plogin')
link.click()
time.sleep(1)

username = driver.find_element_by_id('u')
password = driver.find_element_by_id('p')
username.send_keys('545613')
password.send_keys('afasf213')
button = driver.find_element_by_id('login_button')
button.click()
time.sleep(3)

driver.switch_to.frame(0)
img_div = driver.find_element_by_id('slideBkg')
img_url = img_div.get_attribute('src')
print(img_div, img_url)

conn = pymongo.MongoClient('127.0.0.1', 27017)
urun = conn.urun
urun['qq_img'].insert({"url": img_url})
time.sleep(1)
for i in range(30):
    try:
        refresh = driver.find_element_by_class_name('tcaptcha-embed-refresh')
        refresh.click()
        time.sleep(2)
        img_div = driver.find_element_by_id('slideBkg')
        img_url = img_div.get_attribute('src')
        print(img_div, img_url)
        urun['qq_img'].insert({"url": img_url})
        time.sleep(randint(2, 4))
    except Exception as e:
        time.sleep(randint(2, 4))

        print(e)

#
#
#
# for i in range(5):
#     try:
#         driver.switch_to.frame(i)
#         print('1')
#
#         html = driver.page_source
#         with open('qq_frame_inner_{}.html'.format(i), 'w', encoding='utf-8') as f:
#             f.write(html)
#         login = driver.find_element_by_class_name('tcaptcha-bg')
#         print(login, i)
#         img_div = driver.find_element_by_id('slideBkg')
#         img_url = img_div.get_attribute('src')
#         print(img_div, img_url)
#         time.sleep(2)
#     except Exception as e:
#         print(e)
#         continue
# print('end')












# html = driver.page_source
# print(html)
# with open('qq.html', 'w', encoding='utf-8') as f:
#     f.write(html)
# for i in range(5):
#     try:
#         driver.switch_to.frame(i)
#         print('1')
#
#         html = driver.page_source
#         with open('qq_frame_{}.html'.format(i), 'w', encoding='utf-8') as f:
#             f.write(html)
#         login = driver.find_element_by_class_name('login')
#         print(login, i)
#         action = ActionChains(driver)
#         time.sleep(2)
#     except Exception as e:
#         print(e)
#         continue
# print('end')
# html = driver.page_source
#
# login = driver.find_element_by_class_name('login')
# login.click()
#
# pop = driver.page_source
# print(pop)