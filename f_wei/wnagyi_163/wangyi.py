import time
from random import randint
import pymongo
from selenium import webdriver
from selenium.webdriver.common.action_chains import *
conn = pymongo.MongoClient('127.0.0.1', 27017)

urun = conn.urun
driver = webdriver.Chrome()

url = 'http://reg.163.com/'

driver.get(url)
time.sleep(5)

driver.switch_to.frame(1)
# print(driver.page_source)
# frame =driver.find_element_by_name('')
# driver.switch_to_frame(frame)
# elem = driver.find_element_by_class_name('yidun_tips')
# # x-URS-iframe1531807808317.6755
# print(elem)
html = driver.page_source
with open('wangyi_frame.html', 'w', encoding='utf-8') as f:
    f.write(html)
action = ActionChains(driver)

characters = driver.find_element_by_class_name('yidun_tips')


time.sleep(1)
action.move_to_element(characters).perform()




characters_img = driver.find_element_by_class_name('yidun_bg-img')

urun.wangyi.insert({"url": characters_img.get_attribute('src')})

print(characters.text, characters_img.get_attribute('src'))
refresh = driver.find_element_by_class_name('yidun_refresh')
time.sleep(1)
for i in range(50):
    try:
        refresh.click()
        characters_refresh_img = driver.find_element_by_class_name('yidun_bg-img')
        print(characters_refresh_img)
        time.sleep(randint(2,4))
        urun.wangyi.insert({"url": characters_refresh_img.get_attribute('src')})
    except Exception as e:
        print('error')
        time.sleep(2)
        continue
time.sleep(10)