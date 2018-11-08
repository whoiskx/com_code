# -*- coding: utf-8 -*-
import time

import requests
from selenium import webdriver


def main():
    # requests 乱码
    url = 'https://jin.baidu.com/v/static/mip2/gongjijin-mip2/mip-login.html?wyn=8964e386-6c92-49cf-9c14-21efbdf1e0f0'
    headers = {'Host': 'jin.baidu.com', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Referer': 'https://jin.baidu.com/v/static/mip2/gongjijin-mip2/mip-login.html?wyn=5213da38-73b8-48ab-adb0-dfd7b9380aff',
               'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9',
               # 'Cookie': 'HOSUPPORT=1;HISTORY=e2e8e3af6c3a6d456fd968c031;BAIDUID=FA0ACFAAA0FAB0A802684C9C9D4EBF9C:FG=1;Hm_lvt_90056b3f84f90da57dc0f40150f005d5=1541579444,1541579447;STOKEN=a0a01a003015917bac672d286102c3279df779b1a76af37d6a13e3fa2f3262a3;pplogid=8442f48LCMmdMiYCRZKdHM0m9rQt7KUXz8Iodu8xFOYbHhA%3D;Hm_lpvt_90056b3f84f90da57dc0f40150f005d5=1541579447;UBI=fi_PncwhpxZ%7ETaKAWOBhHKYW5MBzJRbI%7EFE-EIypt5iRS-V-Rn3LHhZHjSRlIQpuEONOx96wfj2YeeNxqMT;USERNAMETYPE=1;SAVEUSERID=5ebbf0a04cf701610b;BDUSS=VgzOW04dGR4RHh2SWg5OEM0TTNRYmVVQk9rbzViQXBLN1FZRTFPZ3ViVy1Md3BjQVFBQUFBJCQAAAAAAAAAAAEAAAC~B-EpZGJ3aHkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL6i4lu-ouJbW;PTOKEN=19e568f55b4b5ba78d7d33d8761eac4b'
    }
    params = {
        'wyn': 'db8cd87d-eaad-4d81-bacf-ee08f5e01079'
    }
    r = requests.get(url)
    r.encoding = 'utf-8'
    with open('homepage.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
    #
    # print(r.text)

    driver = webdriver.Chrome()
    time.sleep(1)
    url = 'https://jin.baidu.com/v/static/mip2/gongjijin-mip2/mip-login.html?wyn=8964e386-6c92-49cf-9c14-21efbdf1e0f0'

    # cookie1 = {'domain': '.baidu.com', 'expiry': 1573113192.868555, 'httpOnly': False, 'name': 'BAIDUID', 'path': '/',
    #            'secure': False, 'value': '03C7E86328698E1E461BECA47988E94B:FG=1'}
    # cookie2 = {'domain': '.baidu.com', 'expiry': 1800777207.326466, 'httpOnly': True, 'name': 'BDUSS', 'path': '/',
    #            'secure': False,
    #            'value': 'FctS1NFbnJtc05FVjZ5NWVSenpieDNoem5McEVYN1NuZWR2UFJaTE1majRKZ3BjQVFBQUFBJCQAAAAAAAAAAAEAAACn~KxI0MfG2rDLX7K7t8W82QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPiZ4lv4meJbN'}

    cookie1 = {'name': 'BAIDUID', 'value': '03C7E86328698E1E461BECA47988E94B:FG=1'}
    cookie2 = {'name': 'BDUSS',
               'value': 'FctS1NFbnJtc05FVjZ5NWVSenpieDNoem5McEVYN1NuZWR2UFJaTE1majRKZ3BjQVFBQUFBJCQAAAAAAAAAAAEAAACn~KxI0MfG2rDLX7K7t8W82QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPiZ4lv4meJbN'}
    driver.get(url)
    time.sleep(1)
    driver.add_cookie({'name': 'BAIDUID', 'value': '03C7E86328698E1E461BECA47988E94B:FG=1'})
    driver.add_cookie(cookie2)
    time.sleep(1)

    driver.get(url)
    time.sleep(1)
    login = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_3__footerULoginBtn"]')
    time.sleep(0.5)
    login.click()

    username = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_3__userName"]')
    password = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_3__password"]')
    username.send_keys('dbwhy')
    time.sleep(1)
    password.send_keys('tb1232')
    time.sleep(0.2)
    password.send_keys('58456')
    time.sleep(3)
    # driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_3__submit"]').click()
    driver.find_element_by_id('TANGRAM__PSP_3__submit').click()
    # while True:
    #     try:
    #         time.sleep(1)
    #         driver.find_element_by_xpath('//*[@id="TANGRAM__22__header_a"]').click()
    #         # // *[ @ id = "TANGRAM__23__header_a"]
    #         time.sleep(1)
    #         driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_3__submit"]').click()
    #     except Exception as e:
    #         print(e)
    #     time.sleep(1)
    # get the session cookie  
    time.sleep(1)
    # for item in driver.get_cookies():
    #     cookie = item["name"] + "=" + item['value']

    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    # print cookie  
    cookiestr = ';'.join(item for item in cookie)
    print(cookiestr)
    print('cookies_dict: {}'.format(driver.get_cookies()))
    time.sleep(5)


if __name__ == '__main__':
    main()
