import redis, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

def handle(task):
    print(task)
    url = task.decode()
    driver.get(url)
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, 'title')))


def main():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    while 1:
        result = r.blpop('fb_home_url', 0)
        handle(result[1])


if __name__ == "__main__":
    main()