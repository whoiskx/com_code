import time
from random import randint
import pymongo
from selenium import webdriver
from selenium.webdriver.common.action_chains import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

conn = pymongo.MongoClient('127.0.0.1', 27017)
urun = conn.urun
driver = webdriver.Chrome()

url = 'http://reg.163.com/'
driver.get(url)
time.sleep(5)

driver.switch_to.frame(1)

action = ActionChains(driver)

characters = driver.find_element_by_class_name('yidun_tips')
time.sleep(1)
action.move_to_element(characters).perform()

characters_img = driver.find_element_by_class_name('yidun_bg-img')
urun.wangyi.insert({"url": characters_img.get_attribute('src')})

print(characters.text, characters_img.get_attribute('src'))
refresh = driver.find_element_by_class_name('yidun_refresh')
time.sleep(1)
for i in range(500):
    try:
        refresh.click()
        time.sleep(randint(1,3))
        # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_bg-img')))
        characters_refresh_img = driver.find_element_by_class_name('yidun_bg-img')
        print(characters_refresh_img)
        urun.wangyi500.insert({"url": characters_refresh_img.get_attribute('src')})
    except Exception as e:
        print('error', e)
        time.sleep(2)
        continue
print('end')