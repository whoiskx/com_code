import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import *
driver = webdriver.Chrome()

url = 'http://www.qq.com/'

driver.get(url)
time.sleep(5)
html = driver.page_source

login = driver.find_element_by_class_name('login')
login.click()

pop = driver.page_source
print(pop)