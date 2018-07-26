import redis, time
from selenium import webdriver

driver = webdriver.Chrome()

def handle(task):
    print(task)
    url = task.decode()
    driver.get(url)
    time.sleep(4)


def main():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    while 1:
        result = r.blpop('fb_home_url', 0)
        handle(result[1])


if __name__ == "__main__":
    main()