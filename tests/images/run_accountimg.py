# -*- coding: utf-8 -*-
import base64
import json
from flask import Flask, request, jsonify, send_from_directory
import os


class ImageSave(object):
    def __init__(self):
        self.BASE_DIR = r'D:\WXSchedule\Images_tests'
        if not os.path.exists(self.BASE_DIR):
            os.makedirs(self.BASE_DIR)

    def images_to_save(self, account_id, content):
        print(account_id)
        num = int(account_id) // 1000
        IMAGE_DIR = os.path.join(self.BASE_DIR, str(num))
        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR)

        image_path = os.path.join(IMAGE_DIR, str(account_id) + '.jpg')
        try:
            with open(image_path, 'wb') as f:
                f.write(content)
            return {
                'Success': True,
                'Message': '保存成功：{}'.format(image_path),
            }
        except Exception as e:
            print(e)
            return {
                'Success': True,
                'Message': '保存失败：{}'.format(image_path),
            }


app = Flask(__name__)
images = ImageSave()


@app.route('/SaveImage', methods=['POST'])
def save_image():
    if request.method == 'POST':
        data = request.form
        content = base64.b64decode(data.get('content'))
        account_id = data.get('account_id')
        result = images.images_to_save(account_id, content)
        return jsonify(result)


@app.route("/BackImage/<filename>")
def back_image(filename):
    # Images/50000/50000350.jpg
    print('path', filename)
    user_file_dir = r'D:\WXSchedule\Images'
    account_id = filename.replace('.jpg', '')
    num = int(account_id) // 1000
    IMAGE_DIR = os.path.join(user_file_dir, str(num))
    path = os.path.join(IMAGE_DIR, filename)
    print(IMAGE_DIR, filename)
    if IMAGE_DIR and filename:

        if os.path.exists(path):
            return send_from_directory(IMAGE_DIR, filename)
        else:
            # 返回默认图片
            IMAGE_DIR = os.path.join(user_file_dir, '0')
            filename = '0.jpg'
            return send_from_directory(IMAGE_DIR, filename)
    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8009)
