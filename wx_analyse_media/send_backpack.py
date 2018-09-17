import json
import time
import requests
from utils import log
import re
from pyquery import PyQuery as pq


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

    def set_time(self, resp, type=''):
        if type == 'article':
            get_timestramp = re.search('var ct=".*?"', resp.text).group()
            timestramp = re.search('\d+', get_timestramp).group()
            self.time = timestramp + '000'
        if type == 'video':
            get_timestramp = re.search('create_time = ".*?"', resp.text).group()
            timestramp = re.search('\d+', get_timestramp).group()
            self.time = timestramp + '000'

    def create(self, url, name=''):
        self.url = url
        resp = requests.get(self.url)
        e = pq(resp.text)
        # 匹配分享的文章 好像失效
        if 'var ct=' not in resp.text:
            # 第一次看到嫂子的就是她的 晚聊伴夜
            if '此内容因违规无法查看' in e('.title').text():
                self.title = '此内容因违规无法查看'
                return
            if '此内容被投诉且经审核涉嫌侵权，无法查看。' in e('.title').text():
                self.title = '此内容被投诉且经审核涉嫌侵权，无法查看。'
                return
            self.is_share = True
            self.title = e("title").text()
            self.content = e(".share_notice").text()
            time_find = re.search('createDate=new Date\("\d*', resp.text)
            self.time = time_find.group() if time_find else ''
            if '视频' == self.title:
                self.set_time(resp, type='video')
            return
        self.set_time(resp, type='article')
        self.account = e('.profile_meta_value').eq(0).text()
        # if not self.account:
        #     inner_account = re.search('user_name = ".*?"', resp.text)
        #     self.account = inner_account.group().split('"')[1]
        self.title = e('.rich_media_title').text().replace(' ', '')
        self.content = e("#js_content").text().replace('\n', '')
        self.author = e('.profile_nickname').text()


class Account(object):
    def __init__(self):
        # 接口取
        self.account_id = None
        # account.account
        # 微信号(英文)
        self.account = ''
        # 公众号(中文)
        self.name = ''

    def get_account_id(self):
        get_account_id = 'http://60.190.238.178:38010/search/common/wxaccount/select?token=9ef358ed-b766-4eb3-8fde-a0ccf84659db&account={}'.format(
            self.account)
        url_resp = requests.get(get_account_id)
        json_obj = json.loads(url_resp.text)
        results = json_obj.get('results')
        if results:
            # todo 没有accountID 怎么做
            for i in results:
                self.account_id = i.get('AccountID')
                break


class JsonEntity(object):

    def __init__(self, article, account):
        self.url = article.url
        self.title = article.title
        self.content = article.content
        # 公总号名字
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

    def uploads(self, backpack_list):
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
