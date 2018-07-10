import time

from setting import driver_facebook, urun
from selenium import webdriver

driver = webdriver.Chrome()

urls = urun['praise_7_10_2'].find()
for count, u in enumerate(urls) :
    try:

        url = u.get("url")
        print(url)
        driver.get(url)
        time.sleep(2)
        praise = driver.find_element_by_class_name('_2u_j').text
        if '次赞' in praise:
            praise = praise.replace('次赞', '')
        print('第{}次'.format(count), praise)
        time.sleep(2)
        u.update({'praise':praise})
        urun['praise_7_8_praise_2'].insert(u)
    except Exception as e:
        print(e)
        print(u)
        continue

time.sleep(6000)