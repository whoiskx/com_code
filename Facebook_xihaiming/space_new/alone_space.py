from random import randint
import pymongo
from selenium import webdriver
import time

email = 'altantsetseg@post.com'
password = 'Altantsetseg@123'

prefs = {
    'profile.default_content_setting_values':
        {
            'notifications': 2,
            'images': 2,
        }
}
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=options)

# driver = webdriver.Firefox()
driver.implicitly_wait(120)


def execute_times(driver, times=1):
    for i in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # driver.execute_script("window.scrollBy(0,1000)")
        time.sleep(randint(3, 5))
        print('下拉第{}次，总共下拉{}次'.format(i + 1, times))
        # save_number = [10, 200, 250, 280, 300, 400, 500, 550, 600, 700, 800, 900, 1100, 1200, 1500]
        # if i in save_number:
        #     time.sleep(10)
        #     print('begin')
        #     posts_html = driver.page_source
        #     print('end')
        #     time.sleep(20)
        #     with open("posts_index22_{}.html".format(i), "w", encoding='utf-8') as f:
        #         f.write(posts_html)
        #     print('posts_html_22_{}写入文件夹'.format(i))
        #     time.sleep(15)


driver.get("https://www.facebook.com/")
email_text = driver.find_element_by_id("email")
password_text = driver.find_element_by_id('pass')
email_text.send_keys(email)
password_text.send_keys(password)
button = driver.find_element_by_id('loginbutton')
button.click()

try:
    driver.get('https://www.facebook.com/profile.php?id=100018160331338')
    time.sleep(3)
    execute_times(driver, 3000)
    x = int(input("yes or no>"))
    execute_times(driver, x)
    html = driver.page_source
    time.sleep(20)
    with open('index_xihaiming.html', 'w', encoding='utf-8') as f:
        f.write(html)
except Exception as e:
    print('safdafas', e)
    html = driver.page_source
    time.sleep(20)
    with open('index_xihaiming_error.html', 'w', encoding='utf-8') as f:
        f.write(html)
