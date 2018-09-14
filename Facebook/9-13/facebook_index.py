# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from flask import Flask, request, jsonify

app = Flask(__name__)


def main(url):
    driver = webdriver.Chrome()
    url = url
    driver.get(url)
    time.sleep(5)
    # with open('index.html', 'w', encoding='utf-8') as f:
    #     f.write(driver.page_source)
    infos = driver.find_elements_by_class_name('_4bl9')
    praise, friends = '', ''
    for info in infos:
        if '位用户赞了' in info.text:
            praise = info.text.replace(' 位用户赞了', '')
        if '位用户关注了' in info.text:
            friends = info.text.replace(' 位用户关注了', '')
    uid = url.replace('https://www.facebook.com/', '').replace('/', '')
    name = driver.find_element_by_class_name('_64-f').text
    portrait = driver.find_element_by_class_name('_4jhq').get_attribute('src')
    source = 'instagram'
    print('end')
    d = {'uid': uid, 'praise': praise, 'friends': friends, 'name': name, 'portrait': portrait, 'source': source}
    driver.quit()
    print(d)
    return d


@app.route('/get')
def index():
    url = request.args.get('url')
    d = main(url)
    return jsonify(d)


if __name__ == '__main__':
    while True:
        try:
            app.run(host='0.0.0.0', port='8006')
        except Exception as e:
            print(e)
            continue