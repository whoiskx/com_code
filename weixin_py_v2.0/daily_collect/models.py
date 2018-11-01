import json
import os
import random
import time
from ftplib import FTP
import requests

from config import mongo_conn
from utils import log
import re
from pyquery import PyQuery as pq
import datetime
import hashlib
import uuid
import zipfile


class Article(object):
    def __init__(self):
        self.url = ''
        self.account = ''
        self.title = ''
        self.content = ''
        # 作者即公众号名称name
        self.author = ''
        self._from = ''
        self.time = ''
        self.readnum = ''
        self.likenum = ''
        self.is_share = False

    def set_time(self, resp, content_type=''):
        if content_type == 'article':
            get_timestramp = re.search('var ct=".*?"', resp.text).group()
            timestramp = re.search('\d+', get_timestramp).group()
            self.time = timestramp + '000'
        if content_type == 'video':
            get_timestramp = re.search('create_time = ".*?"', resp.text).group()
            timestramp = re.search('\d+', get_timestramp).group()
            self.time = timestramp + '000'

    def create(self, url, account_model):
        self.url = url
        resp = requests.get(self.url)
        if '访问过于频繁，请用微信扫描二维码进行访问' in resp.text:
            log('访问过于频繁，请用微信扫描二维码进行访问')
            time.sleep(600)
            raise RuntimeError('访问过于频繁，请用微信扫描二维码进行访问')
        e = pq(resp.text)
        # 匹配分享的文章 好像失效
        if 'var ct=' not in resp.text:
            # 第一次看到嫂子的就是她的 晚聊伴夜
            if '此内容因违规无法查看' in resp.text:
                self.title = '此内容因违规无法查看'
                return
            if '此内容被投诉且经审核涉嫌侵权' in resp.text:
                self.title = '此内容被投诉且经审核涉嫌侵权，无法查看。'
                return
            self.is_share = True
            # self.title = e("title").eq(0).text()
            self.title = e("title").text()
            self.content = e(".share_notice").text()
            time_find = re.search('createDate=new Date\("\d*', resp.text)
            self.time = time_find.group() if time_find else ''
            if '视频' == self.title:
                self.set_time(resp, content_type='video')

            # if '用腾讯视频观看' in resp.text:
            #     self.set_time(resp, content_type='video')
            return
        if '分享' in e('.share_notice').text():
            self.is_share = True
            # self.content =
        self.set_time(resp, content_type='article')
        self.account = account_model.account
        # if not self.account:
        #     inner_account = re.search('user_name = ".*?"', resp.text)
        #     self.account = inner_account.group().split('"')[1]
        self.title = e('.rich_media_title').text().replace(' ', '')
        # todo 分享的和视频
        self.content = e("#js_content").text().replace('\n', '')
        self.author = account_model.name


class Account(object):
    def __init__(self):
        # 接口取
        self.account_id = ''
        # account.account
        # 微信号(英文)
        self.account = ''
        # 公众号(中文)
        self.name = ''

    def get_account_id(self):
        get_account_id = 'http://60.190.238.178:38010/search/common/wxaccount/select?' \
                         'token=9ef358ed-b766-4eb3-8fde-a0ccf84659db&account={}'.format(
                            self.account)
        url_resp = requests.get(get_account_id)
        json_obj = json.loads(url_resp.text)
        results = json_obj.get('results')
        if results:
            # todo 没有accountID 怎么做
            for result in results:
                if result.get('AccountID'):
                    self.account_id = result.get('AccountID')
                else:
                    # if not account.account_id:
                    log("没有account_id", self.account)
                    db_mongo = mongo_conn()
                    db_mongo['noAccountId'].insert({'account': self.account})
                break


class JsonEntity(object):
    # 发包实体

    def __init__(self, article, account):
        self.url = article.url
        self.title = article.title
        self.content = article.content
        # 公众号名字
        self.author = article.author
        self._from = article.author
        self.time = article.time
        self.views = article.readnum
        self.praises = article.likenum
        self.account_id = str(account.account_id)
        self.site_id = account.account_id
        self.topic_id = 0
        # 采集时间
        self.addon = str(int(time.time()))
        self.task_id = str(account.account_id)
        self.task_name = '微信_' + account.name
        self.account = account.account
        self.id = self.hash_md5(article.title + self.time)

    @staticmethod
    def hash_md5(s):
        import hashlib
        m = hashlib.md5()
        m.update(s.encode(encoding='utf-8'))
        return m.hexdigest()

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def uploads(backpack_list):
        # 上传底层 底层不能接收None，会丢弃
        if backpack_list:
            sever1 = 'http://115.231.251.252:26016/'
            sever2 = 'http://60.190.238.168:38015/'
            body = json.dumps(backpack_list)
            # 保证发送成功
            count = 0
            while True:
                if count > 2:
                    break
                try:
                    log('start uploads')
                    r = requests.post(sever1, data=body)
                    if r.status_code == 200:
                        log('uploads server1 successful')
                except Exception as e:
                    log('uploads http error1', e)
                try:
                    r2 = requests.post(sever2, data=body)
                    if r2.status_code == 200:
                        log('uploads server2 successful')
                        break
                except Exception as e:
                    log('uploads http error2', e)
                count += 1
            log('uploads over')

    @staticmethod
    def uploads_datacenter_relay(backpack_list):
        # 上传数据分发中心
        if backpack_list:
            server = 'http://27.17.18.131:38072'
            server_backup = 'http://119.39.84.12:7104'
            body = json.dumps(backpack_list)
            datacenter_relay = [
                {
                    "headers": {
                        "topic": "Yweixin",
                    },
                    "body": body
                },
            ]
            # 保证发送成功
            count = 0
            while True:
                if count > 2:
                    break
                try:
                    log('start uploads datacenter_relay')
                    r = requests.post(server, data=json.dumps(datacenter_relay))
                    if r.status_code == 200:
                        log('uploads datacenter_relay server successful')
                        break
                    else:
                        log('start uploads datacenter_relay backup')
                        r = requests.post(server_backup, data=json.dumps(datacenter_relay))
                        if r.status_code == 200:
                            log('uploads datacenter_relay server backup successful')
                            break
                        log('数据中心发包异常')
                except Exception as e:
                    log('uploads datacenter_relay http error', e)
                count += 1
            log('uploads datacenter_relay over')

    @staticmethod
    def uploads_datacenter_unity(backpack_list):
        # 上传三合一检索
        if backpack_list:
            sever = 'http://222.184.225.246:8171'
            datacenter_unity = []
            for backpack in backpack_list:
                backpack['body'] = json.loads(backpack['body'])
                datacenter_unity.append({
                    "headers": {
                        "topic": 'proWeixin',
                        "key": backpack['headers']['key'],
                        "timestamp": backpack['headers']['timestamp']
                    },
                    "body": json.dumps({
                        'ID': backpack['body']['ID'],
                        'TaskName': backpack['body']['TaskName'],
                        'Domain': '',
                        'SiteType': 0,
                        'Overseas': 0,
                        'Title': backpack['body']['Title'],
                        'Content': backpack['body']['Content'],
                        'Time': backpack['body']['Time'],
                        'Source': '',
                        'Url': backpack['body']['Url'],
                        'Account': backpack['body']['Account'],
                        'AccountID': backpack['body']['AccountID'],
                        'Author': backpack['body']['Author'],
                        'From': '',
                        'Images': 0,
                        'ImageUrl': '',
                        'PortraitUrl': '',
                        'VideoUrl': '',
                        'Keywords': '',
                        'Language': 0,
                        'TopicName': '',
                        'Views': 0,
                        'Transmits': 0,
                        'Comments': 0,
                        'Praises': 0,
                        'Follows': 0,
                        'Fans': 0,
                        'Blogs': 0,
                        'Sex': 0,
                        'UID': '',
                        'BlogID': '',
                        'Province': '',
                        'City': '',
                        'QuoteBlogID': '',
                        'QuoteUrl': '',
                        'QuoteTime': 0,
                        'QuoteImages': 0,
                        'QuoteVideoUrl': '',
                        'QuoteShortUrl': '',
                        'QuoteUID': '',
                        'QuoteSex': 0,
                        'QuoteProvince': '',
                        'QuoteCity': '',
                        'QuoteFollows': 0,
                        'QuoteFans': 0,
                        'AddOn': backpack['body']['AddOn'],
                        'LongBlogType': 1,
                        'ArticleTitle': '',
                        'ArticleContent': '',
                        'Original': 0,
                        'QuoteContent': '',
                        'QuoteAuthor': '',
                        'QuotePortraitUrl': '',
                        'QuoteImageUrl': '',
                        'QuoteComments': 0,
                        'QuotePraises': 0,
                        'QuoteTransmits': 0,
                        'QuoteSource': '',
                        'Place': '',
                        'DataType': 1003,
                        'EventID': '',
                        'CustomerID': '',
                        'ClassifyID': '',
                        'IsGarbage': 0,
                        'ShortUrl': '',
                        'Tags': '',
                        'DefinedSite': '',
                        'CrawlerType': '1',
                    }, ensure_ascii=False)
                })

            # 保证发送成功
            count = 0
            while True:
                if count > 2:
                    break
                try:
                    log('start uploads datacenter_unity')
                    r = requests.post(sever, data=json.dumps(datacenter_unity))
                    if r.status_code == 200:
                        log('uploads datacenter_unity server1 successful')
                        break
                except Exception as e:
                    log('uploads datacenter_unity http error', e)
                count += 1
            log('uploads datacenter_unity over')

    @staticmethod
    def uploads_ftp(ftp_info, ftp_list):
        # if len(ftp_list) > 15:
        #     ftp_list = ftp_list[:30]
        current_dir = os.getcwd()
        if not os.path.exists(os.path.join(current_dir, 'ftp')):
            os.mkdir('ftp')
        zf_name = str(uuid.uuid1()) + '.zip'
        with zipfile.ZipFile(os.path.join(current_dir, 'ftp', zf_name), mode='w') as zf:
            zf_comment = ftp_info.ftp_note()
            zf.comment = str(zf_comment).encode('gbk')
            for file_name in ftp_list:
                zf.write(os.path.join(current_dir, 'xml', file_name), file_name)
                os.remove(os.path.join(current_dir, 'xml', file_name))
        # time.sleep(5)
        ftp = FTP(timeout=7)  # 设置变量
        ftp.set_debuglevel = 1
        # socket.setdefaulttimeout(timeout)
        # 发包方式一
        try:
            # raise RuntimeError
            ftp.connect("123.182.246.209", 21, timeout=21)  # 连接的ftp sever和端口
            ftp.login("dc5", "qwer$#@!")  # 连接的用户名，密码如果匿名登录则用空串代替即可
        except Exception as e:
            log('ftp 主服务器连接失败，上传备用服务器'.format(e))
            ftp.connect("110.249.163.246", 21, timeout=21)
            ftp.login("dc5", "qwer$#@!")
        # # 发包方式二
        select = random.choice([1, 2])
        if select == 1:
            try:
                ftp.connect("122.224.105.171", 21, timeout=21)  # 连接的ftp sever和端口
                ftp.login("dc5", "qwer$#@!")  # 连接的用户名，密码如果匿名登录则用空串代替即可
            except Exception as e:
                try:
                    log('ftp 主服务器连接失败，上传备用服务器'.format(e))
                    ftp.connect("124.239.144.181", 21, timeout=21)
                    ftp.login("dc15", "qwer$#@!")
                except Exception as e:
                    log('ftp 备用服务器连接失败，上传备备用服务器'.format(e))
                    ftp.connect("121.28.84.254", 21, timeout=21)
                    ftp.login("dc15", "qwer$#@!")
        else:
            try:
                ftp.connect("122.224.105.174", 21, timeout=21)  # 连接的ftp sever和端口
                ftp.login("dc5", "qwer$#@!")  # 连接的用户名，密码如果匿名登录则用空串代替即可
            except Exception as e:
                try:
                    log('ftp 主服务器连接失败，上传备用服务器'.format(e))
                    ftp.connect("124.239.144.181", 21, timeout=21)
                    ftp.login("dc45", "qwer$#@!")
                except Exception as e:
                    log('ftp 备用服务器连接失败，上传备备用服务器'.format(e))
                    ftp.connect("121.28.84.254", 21, timeout=21)
                    ftp.login("dc45", "qwer$#@!")

        filepath = '/' + datetime.datetime.now().strftime("%Y%m%d")
        # filename = uuid.uuid1()
        filename = zf_name
        log(filename)
        cmd = 'STOR /{}/{}'.format(filepath, filename)
        try:
            ftp.storbinary(cmd, open('{}/ftp/{}'.format(current_dir, filename), 'rb'))
        except Exception as e:
            log('上传ftp异常:', e)
        log('上传成功')
        # 删除ftp文件
        # os.remove('{}/ftp/{}'.format(current_dir, filename))


class Backpack(object):
    # 首字母大写兼容发包字段
    def __init__(self):
        self.ID = ''
        self.Account = ''
        self.TaskID = ''
        self.TaskName = ''
        self.AccountID = ''
        self.SiteID = ''
        self.TopicID = ''
        self.Url = ''
        self.Title = ''
        self.Content = ''
        self.Author = ''
        self.Time = ''
        self.AddOn = ''
        self.Tags = ''
        self.DefinedSite = ''
        self.CrawlerType = ''

    def create(self, entity):
        self.ID = entity.id
        self.Account = entity.account
        self.TaskID = entity.task_id
        self.TaskName = entity.task_name
        self.AccountID = entity.account_id
        self.SiteID = int(entity.site_id) if entity.site_id else ''
        self.TopicID = 0
        self.Url = entity.url
        self.Title = entity.title
        self.Content = entity.content
        self.Author = entity.author
        self.Time = int(entity.time) if entity.time else ''
        self.AddOn = int(entity.addon + '000')
        self.CrawlerType = '1'

    def to_dict(self):
        return self.__dict__

    def create_backpack(self):
        uploads_body = {
            "headers": {
                "topic": "weixin",
                "key": self.ID,
                "timestamp": int(time.time()),
            }
        }
        uploads_body.update({'body': json.dumps(self.to_dict())})
        return uploads_body


class Ftp(object):
    def __init__(self, entity):
        # 对应的服务器字段  publistTime 发文时间， collectTime和addonTime都是采集时间 大概三分钟延迟
        self.id = int(entity.account_id)
        self.url = entity.url
        self.title = entity.title
        self.content = entity.content
        self.author = entity.author
        # todo entity.time 为'' 原因文章被删
        self.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(entity.time[:-3]))) if entity.time else ''
        self.account = entity.account

    @staticmethod
    def hash_md5(s):
        m = hashlib.md5()
        m.update(s.encode())
        return m.hexdigest() + '.xml'

    def ftp_dict(self):
        return self.__dict__

    def ftp_note(self):
        note = {
            # 任务ID
            "id": self.id,
            # 任务名
            "name": "微信_{}".format(self.author),
            # 网站名
            "groupName": "微信",
            # 是否境外站点
            "overseas": False,
            # 站点类型
            "category": 14,
            # 站点语言
            "language": 1,
            # 数据类型
            "structure": 1,
            # PageRank
            "pr": 6,
            # 标签id
            "tagID": 0,
            # 是否是首页
            "top": False,
            # 是否是首页
            "home": 0,
            "channel": 20,
            # 采集时间,抓取的时间
            "addon": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        note_json = json.dumps(note, ensure_ascii=False)
        return str(note_json)

    #
    # def create_xml(file_name):
    #     data = etree.Element("data")
    #     for k, v in infos.items():
    #         sub_tag = etree.SubElement(data, k)
    #         if 'time' in k:
    #             sub_tag.text = v
    #             continue
    #         title_txt = str(v)
    #         title_txt = etree.CDATA(title_txt)
    #         sub_tag.text = title_txt
    #     dataxml = etree.tostring(data, pretty_print=True, encoding="UTF-8", method="xml", xml_declaration=True,
    #                              standalone=None)
    #     print(dataxml.decode("utf-8"))
    #     etree.ElementTree(data).write(file_name, encoding='utf-8', pretty_print=True)
    #
    #
    # def create_zip(file_name, f):
    #     # zf = zipfile.ZipFile('4041070c-bd83-11e8-af9f-fc017c3bd1b0.zip', 'r')
    #     print('creating archive')
    #     zf_name = str(uuid.uuid1())
    #     with zipfile.ZipFile('{}.zip'.format(zf_name), mode='w') as zf:
    #         zf_comment = f.ftp_note()
    #         zf.comment = str(zf_comment).encode('gbk')
    #         zf.write(file_name)
