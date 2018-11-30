import time

from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# --no-sandbox 会导致 webdriver无法退出
# chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(chrome_options=chrome_options)
# print("get dirver")
# driver.get('https://www.baidu.com/')
# time.sleep(1)
# driver.save_screenshot('baidu.png')
# print('OK')
# driver.quit()
for i in range(30):
    driver.get('https://weixin.sogou.com/weixin?type=1&s_from=input&query=yqcc0353&ie=utf8&_sug_=n&_sug_type_=')
    if '搜公众号' not in driver.page_source:
        # log.info('当前页面{}'.format(self.driver.page_source))
        print('搜公众号 不在页面中验证失败')
    time.sleep(0.4)
driver.save_screenshot('sougou.png')
print('OK')