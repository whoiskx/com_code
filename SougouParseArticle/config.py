# -*- coding: utf-8 -*-
import os

# 打码平台参数配置
# 接口URL
DYTRY_APIURL = 'http://api.dytry.com/ocr.json'
# 用户名
DYTRY_USERNAME = 'uruntest'
# 用户密码
DYTRY_PASSWORD = '0763!@#'
# 题目类型
DYTRY_TYPEID = 9999
# 软件ID
DYTRY_SOFTID = 1107
# 软件KEY
DYTRY_SOFTKEY = '34af19d2ee35e938dbbdc0336eb730cb'

# Mongodb参数配置
# Mongodb ip
MONGO_HOST = '120.78.237.213'
# Mongodb端口
MONGO_PORT = 27017
# Mongodb数据库  微信
MONGO_DB = 'WeChat'
# Mongodb表集合  单条标题分析
MONGO_COLLECTION = 'single_parse'

# Redis参数配置
# Redis ip
REDIS_HOST = '192.168.1.162'
# Redis数据库
REDIS_DB = 9
# Redis队列名
REDIS_QUEUE = 'ArticleId'

# 文件路径参数配置
# 当前路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# 项目图片路径
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
# 验证码保存名称
CAPTCHA_NAME = 'captcha.png'

# 在数据库中查询相标题的数据
# 底层数据查询接口
SELECT_API_URL = 'http://60.190.238.178:38010/search/common/weixin/select'
'''
'sort': 'Time desc',时间倒序排列
'word': '',文章标题字符串
'fl': 'title,content,time',只返回标题，内容，时间（时间戳+000）
'categories':2
'''

# 给前端返回ArticleId的状态
STATUS_API_URL = 'http://58.56.160.39:38012/api/drafts/updateAnalysisStatusByAnalysisId'
'''
'type': 4,  1:博主  2:博文  3:微信公众号  4:微信文章
'analysisId': ArticleId,  分析ArticleId
'status': 1,  分析状态  1:已添加  2:添加失败  3:分析成功  4:分析失败
'''
