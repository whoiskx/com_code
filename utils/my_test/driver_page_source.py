import time

from selenium import webdriver


driver =  webdriver.Chrome()
url = "https://www.baidu.com/"
driver.get(url)
time.sleep(5)
for i in range(5):
    with open('drive_html_{}.html'.format(i), 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    time.sleep(5)