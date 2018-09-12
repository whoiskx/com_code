# -*- coding: utf-8 -*-
import os
import json

import base64

class ImageSave(object):
    def __init__(self):
        self.BASE_DIR = r'D:\WXSchedule\Images'
        if not os.path.exists(self.BASE_DIR):
            os.makedirs(self.BASE_DIR)

    def images_to_save(self, account_id, content):
        print(account_id)
        num = int(account_id) // 1000
        IMAGE_DIR = os.path.join(self.BASE_DIR, str(num))
        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR)

        image_path = os.path.join(IMAGE_DIR, str(account_id)+'.jpg')
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


if __name__ == '__main__':
    content = b''
    images = ImageSave()
    result = images.images_to_save(59508952,content)
    print(json.dumps(result, indent=4, ensure_ascii=False))
