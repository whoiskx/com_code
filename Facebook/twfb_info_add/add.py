import time
from setting import test
from selenium import webdriver
from pyquery import PyQuery as pq
import re
import hashlib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo
from setting import log

print = log

conn = pymongo.MongoClient()
db_mongo = conn.fb_info


class SpaceData(object):
    def __init__(self, author='', post_time='', comment_sum='', share='', praise='', content='',
                 imgurl=''):
        self.author = author
        self.post_time = post_time
        # self.original = original
        self.comment_sum = comment_sum
        # 分享跟转发一致
        self.share = share
        self.praise = praise
        self.content = content
        self.imgurl = imgurl
        # self.transtmis = transtmis

    def obj_to_dict(self):
        return self.__dict__


def login_must(driver):
    return 'login_must'


def link_error(driver):
    return 'link_error'


def md5_content(content):
    m = hashlib.md5()
    m.update(content.encode(encoding="utf-8"))
    return m.hexdigest()


def parse_specedata(post_divs, spacedata):
    for post_details in post_divs:
        post_html = post_details.get_attribute('outerHTML')
        e = pq(post_html)
        title = e('.fcg').text()

        post_time = e('.timestampContent').text()
        content = e('.userContent').text()
        spacedata.post_time = post_time
        spacedata.content = content
        print('\n', post_time, content)

        # 获取点赞 评论
        # todo 当有更多评论时 无法获取准确评论
        praise = e('.UFILikeSentenceText').text()
        share = e('.UFIShareLink').text()
        comment_number = len(e('.UFIComment'))
        comment_sum = comment_number
        comment_more = e('.UFIPagerLink').text()
        if comment_more != '':
            comment_count = re.search('\d{1,5}', comment_more)
            if comment_count is not None:
                comment_sum += int(comment_count.group())
        praise_number = (re.search('\d{1,5}', praise)).group() if (re.search('\d{1,5}', praise)) else 0
        if '、' in praise:
            praise_people = praise.count('、')
            praise_number = int(praise_number) + 1 + praise_people
        spacedata.praise = praise_number
        spacedata.share = (re.search('\d{1,5}', share)).group() if re.search('\d{1,5}', share) else 0
        spacedata.comment_sum = comment_sum
        print(praise, share, comment_sum, '==', )

        # todo 一张图和多张图(内容中附带的图片)
        spacedata.imgurl = e('.scaledImageFitWidth').attr('src')

        return spacedata


def person(driver):
    # 示例 url https://www.facebook.com/pages/BigBus/103163146499275?rf=1660472990883922
    # https://www.facebook.com/pages/BigBus/103163146499275?rf=1660472990883922
    # driver = webdriver.Chrome()
    # driver.get('')
    # todo 可能找不到元素 崩溃；还有一种 点赞评论转发再一起的类型

    # 地方性商家
    spacedata = SpaceData()
    author = driver.find_element_by_class_name('_2i5e').find_element_by_tag_name('h1').text
    headurl = driver.find_element_by_class_name('scaledImageFitWidth').get_attribute('src')
    post_divs = driver.find_elements_by_class_name('userContentWrapper')
    spacedata.author = author
    spacedata.headurl = headurl

    for post_details in post_divs:

        post_html = post_details.get_attribute('outerHTML')
        e = pq(post_html)
        title = e('.fcg').text()

        post_time = e('.timestampContent').text()
        content = e('.userContent').text()
        spacedata.post_time = post_time
        spacedata.content = content
        print('\n', post_time, content)

        # 获取点赞 评论
        praise = e('.UFILikeSentenceText').text()
        share = e('.UFIShareLink').text()
        comment_number = len(e('.UFIComment'))
        comment_sum = comment_number
        comment_more = e('.UFIPagerLink').text()
        if comment_more != '':
            comment_count = re.search('\d{1,5}', comment_more)
            if comment_count is not None:
                comment_sum += int(comment_count.group())
        praise_number = (re.search('\d{1,5}', praise)).group() if (re.search('\d{1,5}', praise)) else 0
        if '、' in praise:
            praise_people = praise.count('、')
            praise_number = int(praise_number) + 1 + praise_people
        spacedata.praise = praise_number
        spacedata.share = (re.search('\d{1,5}', share)).group() if re.search('\d{1,5}', share) else 0
        spacedata.comment_sum = comment_sum
        print(praise, share, comment_sum, '==', )

        # todo 一张图和多张图
        spacedata.imgurl = e('.scaledImageFitWidth').html()

        post_dict = spacedata.obj_to_dict()
        print("result parse_posts_html{}".format(post_dict))

        test['post-8-2'].insert(post_dict)


def group(driver):
    # 群组
    # driver = webdriver.Chrome()
    infos = driver.find_elements_by_class_name('_4bl9')
    praise, friends = '', ''
    for info in infos:
        if '位用户赞了' in info.text:
            praise = info.text.replace(' 位用户赞了', '').replace(',', '')
        if '位用户关注了' in info.text:
            friends = info.text.replace(' 位用户关注了', '').replace(',', '')
    # uid = url.replace('https://www.facebook.com/', '').replace('/', '')
    name = driver.find_element_by_class_name('_64-f').text
    portrait = driver.find_element_by_class_name('_4jhq').get_attribute('src')
    # source = 'instagram'
    d = {'praise': praise, 'friends': friends, 'name': name, 'portrait': portrait,}
    print(d)
    # choice_list = driver.find_elements_by_class_name('_2yau')
    # for choice in choice_list:
    #     # 模板简介 https://www.facebook.com/pg/%E9%A6%99%E6%B8%AFV%E7%85%9E%E5%9C%98-199794133375360/about/?ref=page_internal
    #     if '简介' in choice.text:
    #         print(choice)
    #         choice.click()
    #         WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, '_50f4')))
    #         try:
    #             find_infos = driver.find_elements_by_class_name('_4-u2')
    #             for find_info in find_infos:
    #                 if '更多信息' in find_info:
    #                     expand = driver.find_element_by_class_name('see_more_link_inner')
    #                     if expand:
    #                         expand.click()
    #                     break
    #         except Exception as e:
    #             print('不需要展开')
    #         description = find_info.find_element_by_class_name('_3-8w').text
    #         print("简介")
    #         d.update({'description': description.replace('\n', '')})
    return d


def main(url):
    driver = webdriver.Chrome()
    driver.get(url)
    choice = ''
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'inputtext')))
    try:
        # 需要登录 https://www.facebook.com/joseph.zen.52
        driver.find_element_by_css_selector('._2nlw._2nlv')
        choice = login_must
    except Exception as e:
        pass

    try:
        # 连接错误 https://www.facebook.com/scleung.itvoice2012
        driver.find_element_by_css_selector('._4-dp')
        choice = link_error
    except Exception as e:
        pass

    try:
        # 个人
        driver.find_element_by_css_selector('._2i5e')
        pass
        choice = person
    except Exception as e:
        pass

    try:
        # 群组 https://www.facebook.com/theeclecticsbasement/
        driver.find_element_by_css_selector('._64-f')
        choice = group
    except Exception as e:
        pass

    if choice == group:
        print(choice)
        choice(driver)


def mysql_localhost():
    # MYSQL_HOST = 'localhost'
    # MYSQL_PORT = 3306
    # MYSQL_USER = 'root'
    # MYSQL_PASSWORD = ''
    # MYSQL_DATABASE = 'comm'
    MYSQL_HOST = '120.78.237.213'
    MYSQL_PORT = 8002
    MYSQL_USER = 'yunrun'
    MYSQL_PASSWORD = 'Yunrun2016!@#'
    MYSQL_DATABASE = 'urun_statistic'

    config_mysql = {
        'host': MYSQL_HOST,
        'port': MYSQL_PORT,
        'user': MYSQL_USER,
        'db': MYSQL_DATABASE,
        'passwd': MYSQL_PASSWORD,
        'charset': 'utf8',
    }
    return config_mysql


if __name__ == '__main__':
    mysql_params = mysql_localhost()
    import pymysql

    db = pymysql.connect(**mysql_params)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM `twfb_copy` where Url like '%facebook%';")
    # 9-19 1145 UID Newmacau https://zh-hk.facebook.com/Newmacau/
    items = cursor.fetchmany(1114)
    items = cursor.fetchall()
    driver = webdriver.Chrome()
    for count, item in enumerate(items):
        log('第{}次, '.format(count))
        print(item)
        uid = item[0]
        url = item[2]
        if ('https' not in url) or ('小麗民主教室' in url):
            continue
        # url = 'https://www.facebook.com/pg/dokul1988/about/?ref=page_internal'
        driver.get(url)
        choice = ''
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'inputtext')))

        try:
            # 群组 https://www.facebook.com/theeclecticsbasement/
            driver.find_element_by_css_selector('._64-f')
            info = group(driver)
            # 群租关注是0
            sql = """
                UPDATE twfb_copy SET Name=%s, HeadUrl=%s, Fans=%s, SiteType=4  where UID=%s
            """
            # d = {'praise': praise, 'friends': friends, 'name': name, 'portrait': portrait,}
            # data = {
            #     'UID': item[0],
            #     'Name': item[1],
            #     'Url': item[2],
            #     'HeadUrl': item[3],
            #     'Source': item[4],
            #     'City': item[5],
            #     'Follows': item[6],
            #     'Fans': item[7],
            #     'Posts': item[8],
            #     'Favourites': item[9],
            #     'Description': item[10],
            #     'Sex': item[11],
            #     'SiteType': item[12],
            #
            # }
            # db_mongo['info'].insert(data)
            print('插入成功')
            cursor.execute(sql, (info.get('name'), info.get('portrait'), info.get('friends'), uid))
            print(uid)
            db.commit()
        except Exception as e:
            print('不是群组', e)

