from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()
driver.get("https://www.facebook.com/")

email = driver.find_element_by_id("email")
email.send_keys("574613576@qq.com")
print(email)
password = driver.find_element_by_id('pass')
password.send_keys('jh123258456')

button = driver.find_element_by_id('loginbutton')
button.click()


cookies = driver.get_cookies()
print(type(cookies))
print(cookies)
