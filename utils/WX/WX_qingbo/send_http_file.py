# encoding=utf-8
import json

import requests

body_one = [{'headers': {'topic': 'weixin', 'key': 'aac1c388c4a37df79a06ee9e43082f3f', 'timestamp': 1534325471},
             'body': '{"ID": "aac1c388c4a37df79a06ee9e43082f3f", "Account": "kaichedashen", "TaskID": "124221220", "TaskName": "\\u5fae\\u4fe1_\\u5f00\\u8f66\\u5927\\u795e", "AccountID": "124221220", "SiteID": 124221220, "TopicID": 0, "Url": "http://mp.weixin.qq.com/s?__biz=MzIxNTY4ODc3NQ==&mid=2247485145&idx=1&sn=f1037a13d21708309c242bdb79392689&chksm=979535f1a0e2bce77dba3a87cee28e6c4fa02888024f4e6a8f2598500d5f607c2c4274494d0e&scene=27#wechat_redirect", "Title": "\\u5f00\\u8f66\\u8ffd\\u5c3e\\u9047\\u731b\\u517d\\uff0c\\u53f8\\u673a\\u63a5\\u8fde\\u88ab\\u72e0\\u63cd\\uff01", "Content": "\\u70b9\\u201c\\u5f00\\u8f66\\u5927\\u795e\\u201d\\u514d\\u8d39\\u5173\\u6ce8\\uff0c\\u7f6e\\u9876\\u516c\\u4f17\\u53f7", "Author": "\\u5f00\\u8f66\\u5927\\u795e", "Time": 1534247456000, "AddOn": 1534325471000}'},
            {'headers': {'topic': 'weixin', 'key': 'fb6e06c193d69cea3d7db74dc5b1e666', 'timestamp': 1534325471},
             'body': '{"ID": "fb6e06c193d69cea3d7db74dc5b1e666", "Account": "kaichedashen", "TaskID": "124221220", "TaskName": "\\u5fae\\u4fe1_\\u5f00\\u8f66\\u5927\\u795e", "AccountID": "124221220", "SiteID": 124221220, "TopicID": 0, "Url": "http://mp.weixin.qq.com/s?__biz=MzIxNTY4ODc3NQ==&mid=2247485138&idx=1&sn=00d7d3797345ac32b3818b4f7f50a21b&chksm=979535faa0e2bcec28216355f610f4914e332a461c7016ebee0c7f90b9e27149e16419f53291&scene=27#wechat_redirect", "Title": "\\u4e09\\u8f6e\\u5927\\u7237\\u58f0\\u4e1c\\u51fb\\u897f\\uff0c\\u8d27\\u8f66\\u53f8\\u673a\\u4e24\\u9762\\u5939\\u51fb\\uff01", "Content": "\\u70b9\\u201c\\u5f00\\u8f66\\u5927\\u795e\\u201d\\u514d\\u8d39\\u5173\\u6ce8\\uff0c\\u7f6e\\u9876\\u516c\\u4f17\\u53f7", "Author": "\\u5f00\\u8f66\\u5927\\u795e", "Time": 1533906273000, "AddOn": 1534325471000}'},
            {'headers': {'topic': 'weixin', 'key': '8e1de2da7f135be6f57df0bcf45067bb', 'timestamp': 1534325472},
             'body': '{"ID": "8e1de2da7f135be6f57df0bcf45067bb", "Account": "kaichedashen", "TaskID": "124221220", "TaskName": "\\u5fae\\u4fe1_\\u5f00\\u8f66\\u5927\\u795e", "AccountID": "124221220", "SiteID": 124221220, "TopicID": 0, "Url": "http://mp.weixin.qq.com/s?__biz=MzIxNTY4ODc3NQ==&mid=2247485134&idx=1&sn=875224e6b943163136c7480b357e329a&chksm=979535e6a0e2bcf03a9e882b4a56126b1506714a8d77e75a797d4fc80d42f4d8f9d3b3151c5a&scene=27#wechat_redirect", "Title": "\\u5f00\\u4e0a\\u5bbe\\u5229\\u5f88\\u81a8\\u80c0\\uff0c\\u4e00\\u8def\\u98d9\\u6b4c\\u771f\\u662f\\u6d6a\\uff01", "Content": "\\u70b9\\u201c\\u5f00\\u8f66\\u5927\\u795e\\u201d\\u514d\\u8d39\\u5173\\u6ce8\\uff0c\\u7f6e\\u9876\\u516c\\u4f17\\u53f7\\u7231\\u4f60\\u4eec\\uff0c\\u4e48\\u4e48\\u54d2\\uff01", "Author": "\\u5f00\\u8f66\\u5927\\u795e", "Time": 1533819730000, "AddOn": 1534325472000}'},
            {'headers': {'topic': 'weixin', 'key': '820bf386b3582517212875a5aaf130df', 'timestamp': 1534325472},
             'body': '{"ID": "820bf386b3582517212875a5aaf130df", "Account": "kaichedashen", "TaskID": "124221220", "TaskName": "\\u5fae\\u4fe1_\\u5f00\\u8f66\\u5927\\u795e", "AccountID": "124221220", "SiteID": 124221220, "TopicID": 0, "Url": "http://mp.weixin.qq.com/s?__biz=MzIxNTY4ODc3NQ==&mid=2247485121&idx=1&sn=6cac2651044f718030e92a16f4ac3025&chksm=979535e9a0e2bcffcca3820f2164c9b2535e5e5987fd20dc3829b0a9de366391f1a575501266&scene=27#wechat_redirect", "Title": "\\u5f00\\u8f66\\u52a0\\u585e\\u72af\\u4f17\\u6012\\uff0c\\u53f8\\u673a\\u4e09\\u82f1\\u6218\\u5415\\u5e03\\uff01", "Content": "\\u70b9\\u201c\\u5f00\\u8f66\\u5927\\u795e\\u201d\\u514d\\u8d39\\u5173\\u6ce8\\uff0c\\u7f6e\\u9876\\u516c\\u4f17\\u53f7", "Author": "\\u5f00\\u8f66\\u5927\\u795e", "Time": 1533640003000, "AddOn": 1534325472000}'},
            {'headers': {'topic': 'weixin', 'key': '99194033532625fcb27f9d40d6deb409', 'timestamp': 1534325473},
             'body': '{"ID": "99194033532625fcb27f9d40d6deb409", "Account": "kaichedashen", "TaskID": "124221220", "TaskName": "\\u5fae\\u4fe1_\\u5f00\\u8f66\\u5927\\u795e", "AccountID": "124221220", "SiteID": 124221220, "TopicID": 0, "Url": "http://mp.weixin.qq.com/s?__biz=MzIxNTY4ODc3NQ==&mid=2247485117&idx=1&sn=924a9006861c5e4c69c2d7feeef9a3ae&chksm=97953595a0e2bc8312183ec206035b4a1f2f5c85c4cd152dbe84246b70fd5152356542280c59&scene=27#wechat_redirect", "Title": "\\u5f00\\u8f66\\u8d85\\u901f\\u5feb\\u5982\\u98ce\\uff0c\\u4e0d\\u6599\\u8ffd\\u5c3e\\u4e00\\u573a\\u7a7a\\uff01", "Content": "\\u70b9\\u201c\\u5f00\\u8f66\\u5927\\u795e\\u201d\\u514d\\u8d39\\u5173\\u6ce8\\uff0c\\u7f6e\\u9876\\u516c\\u4f17\\u53f7", "Author": "\\u5f00\\u8f66\\u5927\\u795e", "Time": 1533129696000, "AddOn": 1534325473000}'},
            {'headers': {'topic': 'weixin', 'key': 'fa1a96de524cb10e48ff3607f0b5b066', 'timestamp': 1534325473},
             'body': '{"ID": "fa1a96de524cb10e48ff3607f0b5b066", "Account": "kaichedashen", "TaskID": "124221220", "TaskName": "\\u5fae\\u4fe1_\\u5f00\\u8f66\\u5927\\u795e", "AccountID": "124221220", "SiteID": 124221220, "TopicID": 0, "Url": "http://mp.weixin.qq.com/s?__biz=MzIxNTY4ODc3NQ==&mid=2247485113&idx=1&sn=bc0830d82f1fc0c4f441fa22c55b3fdc&chksm=97953591a0e2bc8753727feed6dd6871ab08324e02f574f49a0b2556cfcee15e79a23c6693af&scene=0#rd", "Title": "\\u6a2a\\u7a7f\\u9a6c\\u8def\\u4e3a\\u6240\\u6b32\\u4e3a\\uff0c\\u6469\\u6258\\u53f8\\u673a\\u8d3c\\u558a\\u6349\\u8d3c\\uff01", "Content": "\\u70b9\\u201c\\u5f00\\u8f66\\u5927\\u795e\\u201d\\u514d\\u8d39\\u5173\\u6ce8\\uff0c\\u7f6e\\u9876\\u516c\\u4f17\\u53f7", "Author": "\\u5f00\\u8f66\\u5927\\u795e", "Time": 1532776347000, "AddOn": 1534325473000}'},
            {'headers': {'topic': 'weixin', 'key': '148929b2b73cbb5fd3df9182575a4e37', 'timestamp': 1534325473},
             'body': '{"ID": "148929b2b73cbb5fd3df9182575a4e37", "Account": "kaichedashen", "TaskID": "124221220", "TaskName": "\\u5fae\\u4fe1_\\u5f00\\u8f66\\u5927\\u795e", "AccountID": "124221220", "SiteID": 124221220, "TopicID": 0, "Url": "http://mp.weixin.qq.com/s?__biz=MzIxNTY4ODc3NQ==&mid=2247485109&idx=1&sn=f1365da118c769af8e1811a2c290213b&chksm=9795359da0e2bc8b42a6af7cadd93281d740f5a8e716a32568f457d62e182e0adb0040147fd1&scene=27#wechat_redirect", "Title": "\\u96e8\\u5929\\u5f00\\u8f66\\u7535\\u95ea\\u96f7\\u9e23\\uff0c\\u5927\\u5a76\\u5c31\\u8981\\u6253\\u62b1\\u4e0d\\u5e73\\uff01", "Content": "\\u70b9\\u201c\\u5f00\\u8f66\\u5927\\u795e\\u201d\\u514d\\u8d39\\u5173\\u6ce8\\uff0c\\u7f6e\\u9876\\u516c\\u4f17\\u53f7", "Author": "\\u5f00\\u8f66\\u5927\\u795e", "Time": 1532440292000, "AddOn": 1534325473000}'},
            {'headers': {'topic': 'weixin', 'key': '5ef8cc86f4a9b75adfeec392bf92a063', 'timestamp': 1534325474},
             'body': '{"ID": "5ef8cc86f4a9b75adfeec392bf92a063", "Account": "kaichedashen", "TaskID": "124221220", "TaskName": "\\u5fae\\u4fe1_\\u5f00\\u8f66\\u5927\\u795e", "AccountID": "124221220", "SiteID": 124221220, "TopicID": 0, "Url": "http://mp.weixin.qq.com/s?__biz=MzIxNTY4ODc3NQ==&mid=2247485099&idx=1&sn=a383204ce893899a582cef2678c11a76&chksm=97953583a0e2bc95fdd9a0cec50c8ffdbfd74f9657ee06363aafd3a4aba29644ed26474f5870&scene=27#wechat_redirect", "Title": "\\u6df1\\u591c\\u53d1\\u8f66\\u76f4\\u5192\\u6c57\\uff0c\\u73a9\\u8f66\\u7684\\u4f60\\u5feb\\u6765\\u770b\\uff01", "Content": "\\u2191\\u2191\\u2191\\u957f\\u6309\\u4e0a\\u65b9\\u4e8c\\u7ef4\\u7801\\u8bc6\\u522b\\u5173\\u6ce8\\u770b\\u7cbe\\u5f69\\u8282\\u76ee\\u89c6\\u9891\\u660e\\u5929\\u66f4\\u65b0\\uff0c\\u8c22\\u8c22\\u60a8\\u5bf9\\u5a76\\u7684\\u652f\\u6301\\uff01", "Author": "\\u5f00\\u8f66\\u5927\\u795e", "Time": 1532347934000, "AddOn": 1534325474000}'},
            {'headers': {'topic': 'weixin', 'key': '9544b03468144d75867ea6cd11c26dbc', 'timestamp': 1534325474},
             'body': '{"ID": "9544b03468144d75867ea6cd11c26dbc", "Account": "kaichedashen", "TaskID": "124221220", "TaskName": "\\u5fae\\u4fe1_\\u5f00\\u8f66\\u5927\\u795e", "AccountID": "124221220", "SiteID": 124221220, "TopicID": 0, "Url": "http://mp.weixin.qq.com/s?__biz=MzIxNTY4ODc3NQ==&mid=2247485090&idx=1&sn=d6ce28ee60223a33c5f4af58cf5e52a1&chksm=9795358aa0e2bc9c26d6b3875d1ecbd61f12f35363a60e86cc0add3ae2491f1fd87acbcefc43&scene=0#rd", "Title": "\\u7535\\u52a8\\u6469\\u6258\\u6ee1\\u8857\\u7a9c\\uff0c\\u65e0\\u5948\\u649e\\u65ad\\u8def\\u706f\\u6746\\uff01", "Content": "\\u70b9\\u201c\\u5f00\\u8f66\\u5927\\u795e\\u201d\\u514d\\u8d39\\u5173\\u6ce8\\uff0c\\u7f6e\\u9876\\u516c\\u4f17\\u53f7", "Author": "\\u5f00\\u8f66\\u5927\\u795e", "Time": 1532174210000, "AddOn": 1534325474000}'},
            {'headers': {'topic': 'weixin', 'key': '727134fc7fe2143bcff84d0608f2889c', 'timestamp': 1534325475},
             'body': '{"ID": "727134fc7fe2143bcff84d0608f2889c", "Account": "kaichedashen", "TaskID": "124221220", "TaskName": "\\u5fae\\u4fe1_\\u5f00\\u8f66\\u5927\\u795e", "AccountID": "124221220", "SiteID": 124221220, "TopicID": 0, "Url": "http://mp.weixin.qq.com/s?__biz=MzIxNTY4ODc3NQ==&mid=2247485080&idx=1&sn=fdff06a29c6b891412df1787d3239b9a&chksm=979535b0a0e2bca6f9df1cab2b95874636b7832bff802e79f4e7ce76e2d5a087177cda7713e1&scene=27#wechat_redirect", "Title": "\\u5f00\\u8f66\\u8d85\\u8f7d\\u538b\\u584c\\u6865\\uff0c\\u53f8\\u673a\\u7ffb\\u6eda\\u65e0\\u5904\\u9003\\uff01", "Content": "\\u70b9\\u201c\\u5f00\\u8f66\\u5927\\u795e\\u201d\\u514d\\u8d39\\u5173\\u6ce8\\uff0c\\u7f6e\\u9876\\u516c\\u4f17\\u53f7", "Author": "\\u5f00\\u8f66\\u5927\\u795e", "Time": 1531914462000, "AddOn": 1534325475000}'}]

url0 = 'http://101.71.28.12:12007/'
url1 = 'http://115.231.251.252:26016/'
url2 = 'http://60.190.238.168:38015/'
body = json.dumps(body_one)

# body = body_one
print(body)

r = requests.post(url0, data=body)
print(r.status_code)
print(r.text)

url = 'http://27.17.18.131:38072'
r = requests.post(url1, data=body)
print(r.status_code)
print(r.text)

print("=====")
r2 = requests.post(url2, data=body)
print(r2.status_code)
print(r2.text)
