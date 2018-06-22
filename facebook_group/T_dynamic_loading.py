import time
from random import randint

from selenium import webdriver
from setting import driver_facebook
driver = driver_facebook()

driver.get("https://www.facebook.com/groups/southmongoliasupport/")

time.sleep(2)
try:
    def execute_times(times):
        for i in range(times + 1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(randint(1, 3))
    execute_times(2000)

    html=driver.page_source
    print(html)
except Exception as e:
    print(e)
finally:
    with open("post2.html", 'w', encoding='utf-8') as f:
        f.write(html)
    print("write OK")