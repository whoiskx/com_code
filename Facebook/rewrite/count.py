from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()

from setting import log

count = 0
while True:
    url = 'https://www.facebook.com/permalink.php?story_fbid=2163264660369593&id=188533647842714'
    driver.get(url)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "fwn")))
    Author = driver.find_element_by_class_name('fwb').text
    count += 1
    print(count)
    log(count)