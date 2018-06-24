import re
import time
from random import randint

from selenium import webdriver
from pyquery import PyQuery as pq
from setting import driver_facebook
driver = driver_facebook()

driver.get("https://www.facebook.com/groups/southmongoliasupport/")

time.sleep(2)
format = '%H:%M'
try:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    print("ok")
    all_praise = driver.find_element_by_class_name('_3ohu')
    all_praise.click()

    def execute_times(times):
        for i in range(times + 1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(randint(1, 3))
            value = time.localtime(int(time.time()))
            dt = time.strftime(format, value)
            if dt == "17:50":
                break
            print(i)
    execute_times(490)

    html=driver.page_source
    print(html)


except Exception as e:
    print(e)
finally:
    with open("post_490.html", 'w', encoding='utf-8') as f:
        f.write(html)
    print("write OK")