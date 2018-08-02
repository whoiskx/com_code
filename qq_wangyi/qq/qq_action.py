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

button_block = driver.find_element_by_class_name('tcaptcha-drag-button')
action = ActionChains(driver)            # 实例化一个action对象
action.click_and_hold(button).perform()  # perform()用来执行ActionChains中存储的行为
action.reset_actions()
action.move_by_offset(180, 0).perform()







