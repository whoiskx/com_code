import time

from setting import urun
from selenium import webdriver

driver = webdriver.Chrome()

urls = urun['praise_7_12_julei'].find()
error_count = 0
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
        u.update({'praise': praise})
        urun['praise_7_11_julei_praise_2'].insert(u)
    except Exception as e:
        print("===========")
        error_count += 1
        print(error_count, e)
        print(u)
        u.update({'praise': 0})
        urun['praise_7_11_julei_praise_2'].insert(u)
        continue
print('end')
time.sleep(6000)
# file_name = r'D:\praise_7_11_praise_2.xlsx'
# load_excel(file_name= file_name)