from selenium import webdriver

driver = webdriver.Chrome()
url = "https://www.baidu.com/"
driver.get(url)
print(driver.page_source)

with open("test_baidu.txt", "w", encoding='utf-8') as f:
    f.write(driver.page_source)