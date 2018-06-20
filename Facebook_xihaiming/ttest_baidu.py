# from selenium import webdriver
#
# driver = webdriver.Chrome()
# url = "https://www.baidu.com/"
# driver.get(url)
# print(driver.page_source)
#
# with open("test_baidu.html", "w", encoding='utf-8') as f:
#     f.write(driver.page_source)

from pyquery import PyQuery as pq
#
with open("test_baidu.html", "r", encoding="utf-8") as f:
    html = f.read()

# e = pq(filename="test_baidu.html")
e = pq(html)
body = e(".qrcode-text").text()

print(body)