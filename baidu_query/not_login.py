# -*- coding: utf-8 -*-
import time

from selenium import webdriver


def main():
    cookies_dict = [
        {'domain': '.passport.baidu.com', 'expiry': 1800853366.871097, 'httpOnly': True, 'name': 'HOSUPPORT',
         'path': '/', 'secure': False, 'value': '1'},
        {'domain': '.passport.baidu.com', 'expiry': 1800853374.196449, 'httpOnly': True, 'name': 'HISTORY',
         'path': '/', 'secure': False, 'value': 'e2e8e3af6c3a6d456fd968c031'},
        {'domain': '.baidu.com', 'expiry': 1573189360.535007, 'httpOnly': False, 'name': 'BAIDUID',
         'path': '/', 'secure': False, 'value': '22E5D267BDC5E991FBBDC334A3CA4A1D:FG=1'},
        {'domain': 'passport.baidu.com', 'expiry': 2172373364, 'httpOnly': False, 'name': 'BAIDUID',
         'path': '/', 'secure': True, 'value': '03C7E86328698E1E461BECA47988E94B:FG=1'},
        {'domain': 'passport.baidu.com', 'expiry': 2172373364, 'httpOnly': False, 'name': 'BDUSS',
         'path': '/', 'secure': True,
         'value': 'FctS1NFbnJtc05FVjZ5NWVSenpieDNoem5McEVYN1NuZWR2UFJaTE1majRKZ3BjQVFBQUFBJCQAAAAAAAAAAAEAAACn~KxI0MfG2rDLX7K7t8W82QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPiZ4lv4meJbN'},
        {'domain': '.passport.baidu.com', 'expiry': 1573189366, 'httpOnly': False,
         'name': 'Hm_lvt_90056b3f84f90da57dc0f40150f005d5', 'path': '/', 'secure': False,
         'value': '1541653364,1541653367'},
        {'domain': '.passport.baidu.com', 'expiry': 1800853374.196327, 'httpOnly': True, 'name': 'STOKEN',
         'path': '/', 'secure': True,
         'value': '5a8cc325b015c0bea426a396bdc01373a61576c30f8ca698f861d8d274960709'},
        {'domain': 'passport.baidu.com', 'expiry': 1541660566.962369, 'httpOnly': True, 'name': 'pplogid',
         'path': '/', 'secure': False, 'value': '8397YuzepmKWqu7NeKpS8ao9U9v42pMjG7it4CvvvPZ9dKM%3D'},
        {'domain': '.passport.baidu.com', 'httpOnly': False,
         'name': 'Hm_lpvt_90056b3f84f90da57dc0f40150f005d5', 'path': '/', 'secure': False,
         'value': '1541653367'},
        {'domain': '.passport.baidu.com', 'expiry': 1800853370.543408, 'httpOnly': True, 'name': 'UBI',
         'path': '/', 'secure': False,
         'value': 'fi_PncwhpxZ%7ETaKAaC1RG0p8c3mOHdISwBw0xyQBf63ANM4yI7fF-hMcouuy2rj81yCSkIeQ8-kgBP4v3jR'},
        {'domain': '.passport.baidu.com', 'expiry': 1800853374.19636, 'httpOnly': True,
         'name': 'USERNAMETYPE', 'path': '/', 'secure': False, 'value': '1'},
        {'domain': '.passport.baidu.com', 'expiry': 1800853374.196382, 'httpOnly': True,
         'name': 'SAVEUSERID', 'path': '/', 'secure': False, 'value': '5ebbf0a04cf701610b'},
        {'domain': '.baidu.com', 'expiry': 1800853374.196408, 'httpOnly': True, 'name': 'BDUSS', 'path': '/',
         'secure': False,
         'value': 'h5RUhSa0FHWlRIbllQMHZsbXJ-bGtiMS1DY2xoMG50aUJKU3lZdmtOaH5VQXRjQVFBQUFBJCQAAAAAAAAAAAEAAAC~B-EpZGJ3aHkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH~D41t~w-Nbc2'},
        {'domain': '.passport.baidu.com', 'expiry': 1800853374.196429, 'httpOnly': True, 'name': 'PTOKEN',
         'path': '/', 'secure': True, 'value': 'e1d9bf5a904d56e2c0be4a7be6c00913'}]
    driver = webdriver.Chrome()
    # 要先访问一次这个域名
    # driver.get('https://aso100.com')
    url = 'https://jin.baidu.com/v/static/mip2/gongjijin-mip2/mip-login.html?wyn=8964e386-6c92-49cf-9c14-21efbdf1e0f0'
    driver.get('https://jin.baidu.com/')
    time.sleep(5)
    print('OK')
    for item in cookies_dict:
        driver.add_cookie(
            {
                'domain': item['domain'],
                'name': item['name'],
                'value': item['value'],
                'path': item['path'],
                'expiry': item['expiry'],
                'value': item['value']

            }
        )

        driver.get(url)
        time.sleep(3)
        print(driver.get_cookies())
        input('是否有效')
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()
