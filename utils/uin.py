# -*- coding: utf-8 -*-
wxuin = '1156918861'.encode()
# -*- coding: utf-8 -*-
import base64
import requests

#
# # uin
# uin = base64.b64encode(wxuin)
#
# def convert_to_permanent_url(temp_url):
#     pre_redirect_url = "".join([temp_url, "&uin=", uin])
#     response = requests.head(pre_redirect_url)
#     permanent_url = response.headers['Location']
#     return permanent_url
# temp= 'https://mp.weixin.qq.com/s?src=11&timestamp=1539592850&ver=1183&signature=ZNgK7MzcRo*67n6PDJo7UyPOJKR434yEbN-O3eRO1vNz8as8lIwzIdvC1pO86O5ja31rmbednmNA2dXRJ2pJS-vpfA4n8sykXgMVzGKnhd8kyqGEJbs3Z2-oROa*l4wY&new=1'
# r = convert_to_permanent_url(temp)
# print(r)


s = requests
biz = 'MjM5MTI2MTI0MA=='
key = '8c29667900de4618208d36505adf29934ad9248953f65c288980ca4f1c70088c76a44dce7e3b5f614fa9a58a95b1b06fc9b05d586fbdfee15672b7a69043437e17236b87a029e661acaa5ef7508885e7'
uin = 'MjE0ODcyODk0MA%3D%3D'
wz_url = "http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=%s&uin=%s&key=%s" % (
    biz, uin, key)
print('wz_url', wz_url)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat'}
r = s.get(wz_url, headers=headers, allow_redirects=False)
print(r.text)
print(r.cookies.get_dict())
print(r.headers)
# Cookie: qv_als=jwp0jbsoq3YHVj2IA1153991568770MnXQ==; uin=MTE1NjkxODg2MQ%3D%3D; key=cac12c6c44e53dc8b07562f4e0dfed483f8e5824af42cfa51eafcacae4cc2ca880eccb3c447bece1a1b812b5323eb3928ab811267611134b3d7f7b7aa46ae41d81f654aa6d011bf0fb085bbbb8ceb1bb; pass_ticket=HAlN6i51Cm2o7tEBVlbV8TbH6wA8UxOOV9HpxjEzfPR3SS%2FXZBxuUmG7umnEZRr5
cook_value = ''
for k, v in r.cookies.get_dict().items():
    cook_value += k + '=' + v + '; '
cook_value = cook_value[:-1]
print(cook_value)

cookies = r.cookies
kwargs = {
    '_biz': "MjM5MTI2MTI0MA==",
    'mid': '2655142500',
    'sn': '77fbb51f69117d7b573e17928f1a26ce',
    'idx': '1',
    'is_only_read': 1,
}
biz = "MjM5MTI2MTI0MA=="
url = 'http://mp.weixin.qq.com/mp/getappmsgext?uin={}&key={}'.format(uin, key)
url = url + '__biz=' + biz + '&'
url = url + 'mid=' + kwargs.get('mid', None) + '&'
url = url + 'sn=' + kwargs.get('sn', None) + '&'
url = url + 'idx=' + kwargs.get('idx', None) + '&'
url = url + 'is_need_ad=0'
print(url)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
    'Cookie': 'devicetype=android-23; lang=zh_CN; version=26070334; wap_sid2=COyAzIAIElwyRXhFYXRvTEU4d3l4WE5PT1JjckdoeTJBOWVQSkZ1WF9SOFVIZTctaHNndC0yT1VBUUgzSGtWNnB3cTZnZ3k0bk01c3dRamViZ0RWVXBvOFhsT2FUOU1EQUFBfjCRnqXeBTgMQAo=; wxuin=2148728940'}
r_cookies = requests.post(url, data=kwargs, headers=headers)
print(r_cookies.status_code)
print(r_cookies.text)
