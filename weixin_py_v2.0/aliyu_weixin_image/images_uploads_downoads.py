# -*- coding: utf-8 -*-

import requests
import pymssql

from config import get_mysql_old

log = print
config_mysql = get_mysql_old()

info = {"name": "佛山市华诚餐饮管理有限公司", "account": "fsshccyglyxgs",
        "features": "佛山市华诚餐饮管理有限公司是一家从田头到餐桌,产业链化经营的餐饮管理、饭堂承包与食材配送专家.公司立足佛山,辐射珠三角,为广大企业、学校、机关单位提供安全、营养的食品解决方案.",
        "certified": "佛山市华诚餐饮管理有限公司"}
name = 'afafdfafaff'
info = {'name': '王盐不一样的旅行', 'account': 'w1151788292',
        'features': '博爱、认真、执着、奋进、快速、责任、信守承诺--是我一直坚守的原则.王盐愿意帮助有梦想、有强烈成功欲望并愿意付出实际行动的朋友走向成功;创造辉煌!', 'certified': '',
        'biz': '"MzI4NTIyNDg0Ng=="'}
while True:
    # 查询 name 为公众号
    url_public = 'http://183.131.241.60:38011/MatchAccount?account={}'.format(name)
    result1 = requests.get(url_public)
    info_image = result1.json()
    image_url = info_image.get("imageUrl")
    image_id = info_image.get("id")
    if not image_id:
        # 增源
        db = pymssql.connect(**config_mysql)
        cursor = db.cursor()

        # account_link = e(".tit").find('a').attr('href')
        # homepage = self.s.get(account_link, cookies=self.cookies)
        # # var biz = "MzU0MDUxMjM4OQ==" || ""
        # biz_find = re.search('var biz = ".*?"', homepage.text)
        # biz = biz_find.group().replace('var biz = ', '')
        # info["biz"] = biz
        sql_insert = """
                INSERT INTO WXAccount_copy(Name, Account, CollectionTime, Biz, Feature, Certification)
                VALUES ('{}', '{}', GETDATE(), '{}', '{}', '{}')""".format(info.get('name'), info.get('account'),
                                                                           info.get('biz', ), info.get('features'),
                                                                           info.get('certified'))
        cursor.execute(sql_insert)
        db.commit()
        log('插入数据成功', info.get('name'))
        log("当前账号id为0 需要添加{}".format(name))
        continue
        # add_account(name,info account, url, collectiontime, biz)
        # time.sleep(6)
        # find = get_account(account)
        # if not find:
        #     tinfoime.sleep(6)

    # 假设账号已存在
    url_public = 'http://183.131.241.60:38011/MatchAccount?account={}'.format(name)
    result1 = requests.get(url_public)
    info_image = result1.json()
    image_url = info_image.get("imageUrl")
    image_id = info_image.get("id")
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
            url_save = 'http://183.131.241.60:38011/SaveImage/{}'.format(info_image.get('id'))
            requests.post(url_save)
