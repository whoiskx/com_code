from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyquery import PyQuery as pq
import setting

driver = webdriver.Chrome()
driver.get("https://www.facebook.com/")

email = driver.find_element_by_id("email")
email.send_keys(setting.email)
password = driver.find_element_by_id('pass')
password.send_keys(setting.password)

button = driver.find_element_by_id('loginbutton')
button.click()


url_group = "https://www.facebook.com/groups/southmongoliasupport/about/"
driver.get(url_group)

html = driver.find_element_by_tag_name("html")

with open("index_group", "w") as f:
    f.write(driver.page_source)

# e = pq(driver.page_source)
# name = e(".fsl fwb fcb")
# print(name)
driver.close()
