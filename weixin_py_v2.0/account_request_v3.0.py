# -*- coding: utf-8 -*-
import datetime
import random
import re
import time

import requests
import json
from setting import log
from pyquery import PyQuery as pq
from send_backpack import JsonEntity, Article, Acount, Backpack
from config import get_mysql_new, log
from utils import uploads_mysql

config_mysql = get_mysql_new()


class AccountHttp(object):
    def __init__(self):
        self.url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='
        self.account = ''
        self.name = '田坝微讯' or '大鼎豫剧'

        self.s = requests.Session()
        self.s.keep_alive = False  # 关闭多余连接
        self.s.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Cookie': 'SUV=1528341984202463; SMYUV=1528341984202323; UM_distinctid=163d847f79f2a2-0f26ee9926c89d-5846291c-1fa400-163d847f7a22bf; CXID=4AC31FD8532F021C999088D76F3FB61E; SUID=9FCF2A3B1E20910A000000005B18AA35; IPLOC=CN4401; weixinIndexVisited=1; ABTEST=6|1535333149|v1; ad=71xzSZllll2bQjy@lllllVm9MSYlllllnhr5VZllll9lllll4j7ll5@@@@@@@@@@; JSESSIONID=aaa4lX2_fZMdr5Xv3ABvw; LSTMV=0%2C0; LCLKINT=235; SNUID=9A638690ABAEDE83070339C3ACDDE1AD; sct=168'
        }

    def account_homepage(self):
        # 搜索并进入公众号主页
        search_url = self.url.format(self.name)
        resp_search = self.s.get(search_url, headers=self.headers)


        if 'class="b404-box" id="noresult_part1_container"' in resp_search.text:
            log("找不到该公众号: {}".format(self.name))
            return
        e = pq(resp_search.text)
        if e(".tit").eq(0).text() == self.name:
            account_link = e(".tit").find('a').attr('href')
        else:
            log("不能匹配正确的公众号: {}".format(self.name))
            return
        homepage = self.s.get(account_link)
        if '<title>请输入验证码 </title>' in homepage.text:
            print("出现验码")
            from verification_code import captch_upload_image
            print('------开始处理微信验证码------')
            cert = random.random()
            image_url = 'https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(cert)
            respones = self.s.get(image_url, )
            captch_input = captch_upload_image(respones.content)
            print('------验证码：{}------'.format(captch_input))
            data = {
                'cert': cert,
                'input': captch_input
            }
            respones = self.s.post(image_url, data=data)
            cookies = requests.utils.dict_from_cookiejar(respones.cookies)
            print('adffa', cookies)
            homepage = self.s.get(account_link)
            print('破解验证码之后')
        account = pq(homepage.text)('.profile_account').text().replace('微信号: ', '')
        return homepage.text, account

    def set_name(self):
        url = 'http://124.239.144.181:7114/Schedule/dispatch?type=8'
        resp = self.s.get(url)
        # data 可能为空
        data_json = resp.text.get('data')
        data = json.loads(data_json)
        self.name = data.get('name')
        # print(self.name)
        # return self.name

    def run(self):
        # self.set_name()
        # while True:
        account_list = ['云中燕', '律动青春',
                        '长岭宝宝乐母婴生活馆', '上海足之源足浴用品有限公司', '私人资源杂货铺', 'zz燕子呀', '中浙油', '金欧莱总代', '神秘电影巨星', '郑州幼儿师范高等专科学校招就办',
                        '骄阳图画本', '郑州一中主体课堂', '至尊银座浙皖汇', '湛江幼专中文系', '北京市大兴区长子营镇中心卫生院', '钟吟在线', '快乐将至ing', '方糖老妖日记',
                        '一木之中', '周庄庄', 'zhangsy', '千奇百货', '折中折', '4K', '微凉子珍', '可乐主人', '转转赚', '鱼丸米线的工作室', '鱼丸米线的小窝',
                        '漫长的白日梦', 'ZZZZZZpc', '壮壮壮果屋', '折中哲华北区', '折中哲华东区']
        for name in account_list:
            self.name = name
            html_account = self.account_homepage()
            if html_account:
                html, account_alp = html_account
            else:
                continue
            log('start', self.name)
            items = re.findall('"content_url":".*?,"copyright_stat"', html)
            backpack_list = []
            for page_count, item in enumerate(items):
                url_last = item[15:-18].replace('amp;', '')
                url = 'https://mp.weixin.qq.com' + url_last
                article = Article()
                article.create(url, self.name)
                log('文章标题:', article.title)
                account = Acount()
                account.name = self.name
                account.account = account_alp
                account.get_account_id()

                entity = JsonEntity(article, account)
                backpack = Backpack()
                backpack.create(entity)
                backpack_list.append(backpack.create_backpack())

                # 上传数据库
                sql = '''   
                        INSERT INTO 
                            account_http(article_url, addon, account, account_id, author, id, title) 
                        VALUES 
                            (%s, %s, %s, %s, %s, %s, %s)
                '''
                _tuple = (
                    article.url, datetime.datetime.now(), entity.account, entity.account_id, entity.author, entity.id,
                    entity.title
                )
                uploads_mysql(config_mysql, sql, _tuple)
                # if page_count == 5:
                #     break

        log("发包")
        if entity:
            entity.uploads(backpack_list)


if __name__ == '__main__':
    test = AccountHttp()
    test.run()
