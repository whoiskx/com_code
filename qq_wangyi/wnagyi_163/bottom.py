import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import *
driver = webdriver.Chrome()

def execute_times(driver, times=1):
    for i in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # driver.execute_script("window.scrollBy(0,1000)")
        time.sleep((2))

        print('下拉第{}次，总共下拉{}次'.format(i + 1, times))
url = 'http://reg.163.com/'

driver.get(url)
time.sleep(5)
execute_times(driver, 3)
html = driver.page_source
with open('wangyi_bottom.html', 'w', encoding='utf-8') as f:
    f.write(html)