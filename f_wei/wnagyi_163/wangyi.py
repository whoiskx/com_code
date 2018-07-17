import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import *
driver = webdriver.Chrome()

url = 'http://reg.163.com/'

driver.get(url)
time.sleep(5)
html = driver.page_source
# with open('wangyi.html', 'w', encoding='utf-8') as f:
#     f.write(html)
action = ActionChains(driver)
characters = ''
find_char = driver.find_element_by_class_name('qrMsg')
action.move_to_element(find_char).perform()

try:
    characters = driver.find_element_by_class_name('yidun_tips')
except Exception as e:
    print('first not find')

if characters == '':
    try:
        characters = driver.find_element_by_class_name('yidun_tips__text')
    except Exception as e:
        print('second not find')
time.sleep(1)
action.move_to_element(find_char).perform()
try:
    characters = driver.find_element_by_class_name('yidun_tips')
except Exception as e:
    print('third not find')

if characters is not None:
    try:
        characters = driver.find_element_by_class_name('yidun_tips__text')
    except Exception as e:
        print('fourth not find')


characters_img = driver.find_element_by_class_name('yidun_bg-img')
print(characters.text, characters_img.get_attribute('src'))

time.sleep(10)