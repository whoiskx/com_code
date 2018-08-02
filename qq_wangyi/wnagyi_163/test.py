# # encoding=utf-8
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
#
# browser = webdriver.Chrome()
# # browser.maximize_window()
# browser.get('http://www.uestc.edu.cn/')
# # 方法一：使用find_element_by_link_text找到顶级菜单，并将鼠标移动到上面
# article = browser.find_element_by_link_text(u'学校概况')
# ActionChains(browser).move_to_element(article).perform()
# # 方法二：使用find_element_by_xpath找到顶级菜单，并将鼠标移动到上面
# # article = browser.find_element_by_xpath('//a[contains(@href,"?ch/3")]')
# # ActionChains(browser).move_to_element(article).perform()
# # 方法一：使用find_element_by_link_text找到二级菜单，并点击
# # menu = browser.find_element_by_link_text(u'学校简介')
# # 方法二：使用find_element_by_xpath找到二级菜单，并点击
# menu = browser.find_element_by_xpath('//li[@classes="first odd nth1"]')
# menu.click()

import time
import re
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import *
# driver = webdriver.Chrome()
#
# url = 'http://reg.163.com/'
with open('wangyi.html', 'r', encoding='utf-8') as f:
    html = f.read()
time.sleep(5)
from pyquery import PyQuery as pq
# login = driver.find_element_by_xpath('//*[@id="auto-id-1531807695853"]')
# print(login)e
# article = driver.find_element_by_link_text('请依次点击')
# ActionChains(driver).move_to_element(article).perform()

result = re.findall('<div class="yidun_tips".*?</div>', html)
print(result)
e = pq(html)
characters = e.find(".yidun_tips")


