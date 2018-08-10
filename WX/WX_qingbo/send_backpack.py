import time


class Article(object):
    def __init__(self):
        self.url = ''
        self.title = ''
        self.content = ''
        # 作者即公众号名称
        self.author = ''
        self.From = ''
        self.time = ''

        self.readnum = ''
        self.likenum = ''


class Acount(object):
    def __init__(self):
        # 接口取
        self.account_id = None
        # account.account
        # 微信号
        self.wx_account = ''
        # 公众号名称
        self.name = ''


class JsonEntity(object):

    def __init__(self, article, account):
        self.url = article.url
        self.title = article.title
        self.content = article.content
        self.author = article.author
        self.From = article.author
        self.time = article.time

        self.views = article.readnum
        self.praises = article.likenum

        self.account_id = str(account.account_id)
        self.site_id = account.account_id
        self.topic_id = 0
        self.addon = int(time.time())

        self.task_id = str(account.account_id)
        self.task_name = account.name

        self.account = account.wx_account
        self.id = self.hash_md5(article.title + self.time)

    @staticmethod
    def hash_md5(s):
        import hashlib
        m = hashlib.md5()
        m.update(s.encode(encoding='utf-8'))
        return m.hexdigest()