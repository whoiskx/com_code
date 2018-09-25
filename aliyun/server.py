# -*- coding: utf-8 -*-
import time

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    time.sleep(20)
    return 'OK'



if __name__ == '__main__':
    app.run()
