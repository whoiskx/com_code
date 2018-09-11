# -*- coding: utf-8 -*-
import time

import requests


# 查询公众号

def add_account(self, name, account, url, collectiontime, biz):
    cur = self.__GetConnect()

    sql = """INSERT INTO WXAccount_copy_copy(Name,Account,Url,CollectionTime,Biz)
             VALUES ('{}','{}','{}','{}','{}')""".format(name, account, url, collectiontime, biz)
    try:
        # 执行sql语句
        cur.execute(sql)
        # 提交到数据库执行
        self.conn.commit()
        print('增源：插入成功：{}'.format(account))
    except Exception as e:
        print('增源：插入失败：{}'.format(account))
        print(e)
        # 如果发生错误则回滚
        self.conn.rollback()
    self.conn.close()


def get_account(self, account):
    cur = self.__GetConnect()
    sql = """SELECT * FROM WXAccount_copy_copy WHERE Account = '{}'""".format(account)
    cur.execute(sql)
    result = cur.fetchall()
    self.conn.close()
    return result


account = 'test'
url = 'test'
collectiontime = int(time.time())
biz = 'test'
count = 0
while True:
    count += 1
    if count > 5:
        break
    name = 'gh_2219b94b95b1'
    url_public = 'http://183.131.241.60:38011/MatchAccount?account={}'.format(name)
    result1 = requests.get(url_public)
    info_image = result1.json()
    image_url = info_image.get("imageUrl")
    image_id = info_image.get("id")
    if not image_id:
        # 增源

        add_account(name, account, url, collectiontime, biz)
        time.sleep(6)
        find = get_account(account)
        if not find:
            time.sleep(6)

    if image_url:
        # 有头像 判断图片有效 默认ID一定有
        # url2 = 'http://60.190.238.188:38016/{}'.format(image_url)
        url2 = 'http://183.131.241.60:38011/QueryWeChatImage?id={}'.format(image_id)
        r_img = requests.get(url2)
        if 'Images/0/0.jpg' in r_img.text:
            print('账号:{} 头像失效'.format(name))
            # 保存图像

    else:
        # 没有头像
        # 保存头像
        if info_image.get('id'):
            info_image.get('id')
            url_save = 'http://183.131.241.60:38011/SaveImage/{}'.format(info_image.get('id'))
            requests.post(url_save)
