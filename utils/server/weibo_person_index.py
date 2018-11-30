import re
import time

from flask import Flask, request
from selenium import webdriver
app = Flask(__name__)


def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)

driver = webdriver.Chrome()
driver.get('https://weibo.com/')

@app.route('/')
def hello_world():
    query = request.args
    log(query)
    url = query.get('url')
    driver.get\
        (url)
    time.sleep(5)
    log(driver.title)
    first_post_time = driver.find_element_by_class_name('WB_from').find_element_by_tag_name('a').text
    log(first_post_time)
    return "{'first_post_time': %s}" % first_post_time

@app.route('/hello')
def hello():
    return "hello"


if __name__ == '__main__':
    # config = {
    #     'host': '0.0.0.0',
    #     'port': 2002,
    #     # 'debug': True,
    # }

    config = dict(
        # debug=True,
        host='0.0.0.0',
        port=2000,
    )
    while 1:
        try:
            log('start')
            app.run(**config)
        except Exception as e:
            log(e)
            time.sleep(5)
