import time

from selenium import webdriver

driver = webdriver.Chrome()

driver.get('https://twitter.com/')
skip_login = driver.find_element_by_xpath('//*[@id="doc"]/div/div[1]/div[1]/div[2]/div[2]/div/a[2]')
skip_login.click()

time.sleep(5)
print('begin')

email = driver.find_element_by_class_name('js-username-field')
password = driver.find_element_by_class_name('js-password-field')
login_button = driver.find_element_by_tag_name('button')
email.send_keys('18390553540@163.com')
password.send_keys('tw123258456')
login_button.click()