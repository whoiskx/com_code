# -*- coding: utf-8 -*-

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return 'OK'


if __name__ == '__main__':
    app.run(port=8005)
