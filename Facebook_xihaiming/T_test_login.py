import time
from selenium import webdriver
import json

driver = webdriver.Chrome()

with open("all_friends.txt", 'r', encoding="utf-8") as f:
    results = json.load(f)
print(results, type(results))

for d in results:
    driver.get(d.get("link", ''))
    print(d.get("name"))
    time.sleep(1)
