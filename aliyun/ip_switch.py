import time

import requests
from selenium import webdriver

prefs = {
    'profile.default_content_setting_values':
        {
            'notifications': 2,
            'images': 2,  # 禁止图片
        }
}
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=options)

def login_and_swich_ip(ip):
    url = 'https://signin.aliyun.com/1604195877004448/login.htm?callback=https%3A%2F%2Fdns.console.aliyun.com%2F'
    driver.get(url)
    time.sleep(1)
    login_name = driver.find_element_by_xpath('//*[@id="user_principal_name"]')
    time.sleep(1)
    login_name.clear()
    login_name.send_keys('domain@1604195877004448')
    next_step = driver.find_element_by_xpath('//*[@id="J_FormNext"]/span')
    next_step.click()
    login_passwd = driver.find_element_by_xpath('//*[@id="password_ims"]')
    time.sleep(0.5)
    login_passwd.send_keys('yunrun!@#123')
    time.sleep(1)
    button = driver.find_element_by_xpath('//*[@id="u22"]/input')
    button.click()
    # 进入阿里云
    time.sleep(1)
    close_windows = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[1]/i[1]').click()
    time.sleep(3)
    domin_yun = driver.find_element_by_xpath(
        '//*[@id="container"]/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[3]/td[2]/span[2]/div[1]/a')
    domin_yun.click()
    time.sleep(2)

    change_button = driver.find_element_by_xpath(
        '//*[@id="container"]/div/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[9]/span/span[1]')
    change_button.click()

    # 清空并输入新IP
    ip_input = driver.find_element_by_xpath('//*[@id="value"]')
    ip_input.clear()
#    ip_input.send_keys('1.1.1.1')

    ip_input.send_keys(ip)
    time.sleep(0.5)
    driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[1]/div[3]/div/button[2]').click()


def main():

    while True:
        main_url = 'http://61.164.49.130:19002/test.html'
        backup_url = 'http://124.239.144.163:19002/test.html'
        resp = requests.get(main_url)
        if resp.status_code > 400:


    # 登录
    url = 'https://signin.aliyun.com/1604195877004448/login.htm?callback=https%3A%2F%2Fdns.console.aliyun.com%2F'
    driver.get(url)
    time.sleep(1)
    login_name = driver.find_element_by_xpath('//*[@id="user_principal_name"]')
    time.sleep(1)
    login_name.clear()
    login_name.send_keys('domain@1604195877004448')
    next_step = driver.find_element_by_xpath('//*[@id="J_FormNext"]/span')
    next_step.click()
    login_passwd = driver.find_element_by_xpath('//*[@id="password_ims"]')
    time.sleep(0.5)
    login_passwd.send_keys('yunrun!@#123')
    time.sleep(1)
    button = driver.find_element_by_xpath('//*[@id="u22"]/input')
    button.click()
    # 进入阿里云
    time.sleep(1)
    close_windows = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[1]/i[1]').click()
    time.sleep(3)
    domin_yun = driver.find_element_by_xpath('//*[@id="container"]/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[3]/td[2]/span[2]/div[1]/a')
    domin_yun.click()
    time.sleep(2)

    change_button = driver.find_element_by_xpath('//*[@id="container"]/div/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[9]/span/span[1]')
    change_button.click()

    # 清空并输入新IP
    ip_input = driver.find_element_by_xpath('//*[@id="value"]')
    ip_input.clear()
    ip_input.send_keys('1.1.1.1')
    time.sleep(0.5)
    driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[1]/div[3]/div/button[2]').click()


if __name__ == '__main__':
    main()