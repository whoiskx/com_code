# -*- coding: utf-8 -*-

from flask import Flask,request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        img_byte = request.form.get('content')
        with open('images/xx.jpg', 'wb') as f:
            f.write(img_byte)
        print(img_byte)
    return img_byte or '00'


if __name__ == '__main__':
    app.run()
