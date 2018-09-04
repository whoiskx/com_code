# -*- coding: UTF-8 -*-
import requests

url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E5%A4%A7%E9%BC%8E%E8%B1%AB%E5%89%A7&ie=utf8&_sug_=n&_sug_type_='

headers = {
           # 'Cookie': 'SUV=1528341984202463; SMYUV=1528341984202323; UM_distinctid=163d847f79f2a2-0f26ee9926c89d-5846291c-1fa400-163d847f7a22bf; CXID=4AC31FD8532F021C999088D76F3FB61E; SUID=9FCF2A3B1E20910A000000005B18AA35; IPLOC=CN4401; weixinIndexVisited=1; ABTEST=6|1535333149|v1; ad=71xzSZllll2bQjy@lllllVm9MSYlllllnhr5VZllll9lllll4j7ll5@@@@@@@@@@; sct=132; SNUID=568165754F4B3BFC4E8ADF104FB7AB4F; JSESSIONID=aaa4lX2_fZMdr5Xv3ABvw',

          }
r = requests.get(url)
print(r.text)
# with open("searc.html", 'w', encoding='utf-8') as f:
#     f.write(r.text)
