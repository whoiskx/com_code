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

# SQL server参数配置
# SQL server ip端口
SQL_SERVER_HOST = '183.131.241.60:38019'
# SQL server 用户名
SQL_SERVER_USER = 'oofraBnimdA_gz'
# SQL server 密码
SQL_SERVER_PWD = 'fo(25R@A!@8a823#@%'
# SQL server 数据库  微信
SQL_SERVER_DB = 'Winxin'

# 文件路径参数配置
# 当前路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# 项目文件路径
FILES_DIR = os.path.join(BASE_DIR, 'files')
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)
# 项目图片路径
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
# 验证码保存名称
CAPTCHA_NAME = 'captcha.png'
# 新闻关键词TXT文件完整名称
KEYS_FILE_NAME = 'search_keys.txt'

# 接口参数配置
# 获取AccountID接口
GetAccountId_URL = 'http://60.190.238.178:38010/search/common/wxaccount/select'
GetAccountId_TOKEN = '9ef358ed-b766-4eb3-8fde-a0ccf84659db'

# 微信判重（获取url）接口：主接口
GetCacheWx_URL_main = 'http://47.100.53.87:8008/Schedule/GetCacheWx'
# 微信判重（获取url）接口： 备用接口
GetCacheWx_URL_backup = 'http://183.238.76.203:38015/Schedule/GetCacheWx'

# 微信判重（添加url）接口：主接口
CacheWx_URL_main = 'http://47.100.53.87:8008/Schedule/CacheWx'
# 微信判重（添加url）接口： 备用接口
CacheWx_URL_backup = 'http://183.238.76.203:38015/Schedule/CacheWx'

# 发包接口
SEND_URL_1 = 'http://115.231.251.252:26016'
SEND_URL_2 = 'http://60.190.238.168:38015'

# 1.普通采集  2.元搜索
SOURCENODES = 2
# 1.文章  2.微信  3.微博
SOURCETYPE = 2

# 一次发包大小:3M
MAX_SEND_SIZE = 3 * 1024 * 1024

# 开关参数配置
# 1：任务版本，2：日常采集
DEMO_TYPE = 2
# 是否读取txt里面关键字
TXT_ENABLED = False
# 公众号增源
SOURCE_ADD_ENABLED = False
# 判重
SENTENCED_ENABLED = False
# 发包
SEND_PACKAGE_ENABLED = False
