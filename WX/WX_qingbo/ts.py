# import time
#
# while True:
#
#     try:
#         raise 1 == 2
#     except Exception as e:
#         print('send http error', e)
#     try:
#         print(1)
#     except Exception as e:
#         print(e, 'send http error')
#     print('abv')
#     time.sleep(10)


from selenium import webdriver

driver = webdriver.Chrome()
url = 'https://www.baidu.com/'
driver.get(url)
print