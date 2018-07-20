# coding:utf-8

# import sys
# sys.path.append('../')
from flask import Flask
import time

#
# from Util.GetConfig import GetConfig
#
app = Flask(__name__)

from qq.api import app as catpcha_qq_api

# from wanyi.api import app as captcha_163_api
app.register_blueprint(catpcha_qq_api, url_prefix='/qq')


def run():
    while 1:
        try:
            print('start app...1')
            app.run(port=8356, host='0.0.0.0', debug=True)
        except Exception as e:
            print(e)
            print('sleep...')
            time.sleep(10)


if __name__ == '__main__':
    run()
