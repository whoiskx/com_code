import time

from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# --no-sandbox 会导致 webdriver无法退出
# chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(chrome_options=chrome_options)
print("get dirver")
driver.get('https://www.baidu.com/')
time.sleep(1)
driver.save_screenshot('baidu.png')
print('OK')
driver.quit()
