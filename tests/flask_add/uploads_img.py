# -*- coding: utf-8 -*-
import requests
import base64

#
url = "http://img01.sogoucdn.com/app/a/100520090/oIWsFt-9qc9wQlpNOwJuYnewXRlQ"
r = requests.get(url)
print(r.status_code)
url2 = 'http://58.56.160.39:38012/MediaManager/api/attach/uploadFilesByte'
params = []
#
file_info = {'fileName': "wx_images_test.jpg", 'content': "", 'type': 1}
image_add = 'data:image/jpeg;base64,'

img_stream = base64.b64encode(r.content)
file_info.update({'content':image_add + img_stream.decode('utf-8')})
print(file_info)

# 上传
resp = requests.post(url2, json=[file_info])
print(resp)

print(resp.text)

# import base64
# with open('static/images/test.jpg', 'rb') as f:
#     r = f.read()
# img_stream = base64.b64encode(r)
# file_info.update({'content':img_stream})
# print(file_info)