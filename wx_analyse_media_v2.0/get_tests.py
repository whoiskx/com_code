# -*- coding: utf-8 -*-

account = ['WL-lanlan90', 'zui-kaizhou', 'shudongvivi',
           'jianhu17357515591', 'xy164110901', 'jdzfhk', 'fsshccyglyxgs', 'gh_ccc140cd53fa', 'laosunblog',
           'gh_eb4627ac5dff', 'Terracotta1979', 'SC5046', 'gh_c7cf0416f680', 'qyxbhxx', 'pushan-love',
           'gh_887cecdf76ca', 'gh_033db5fe9c20', 'gh_74b3b2fdd663', 'zju52share', 'jsqjzjjy', 'gh_7439fb177533',
           'Ocean_Warriors', 'futela2018', 'wxnmgltxgbdyzj', 'hjs353', 'Q2blockchain', 'ysy8456', 'gh_3ca6d5ac0bd1',
           'xiaoymsp', 'itASti-TM', 'gh_3b63b4d4ca99', 'xhgczj_123', 'huangtai260', 'enkin8888', 'ZhuHaikjk',
           'wyh2568780976', 'PSTE421261262', 'chaoShanLife520', 'nina17688399260', 'cqww11', 'NIB_DZ_Channel',
           'sixiangcd', 'gh_cb860056b87d', 'Mhuihui0-0', 'hnsxsfzydszdsyb', 'gh_d7252418f9e6', 'gh_2219b94b95b1',
           'jingshenjianbing', 'dgdjsh', 'gh_b7373d9ff0b2', 'gh_698dc9c1bdbb', 'yinyangchashe1', 'gh_f930f004e9ae',
           'gh_d30ee2c6a470', 'gh_ccbdb46e998f', 'gh_5c6abae06e1f', 'gh_7d73a0f8a224']

print(len(account))
import requests

url1 = 'http://127.0.0.1:8008/WeiXinArt/AddAccount?account={}'
url2 = 'http://182.245.126.226:8312/WeiXinArt/AddAccount?account={}'
for i, a in enumerate(account):
    url = url1.format(a)
    r = requests.get(url)
    print(r.text)
    if i > 5:
        break
