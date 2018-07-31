import redis
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


with open('temp.html', 'r', encoding='utf-8') as f:
    html_init = f.read()


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


def parse_post(html=''):
    e = pq(html)
    author = "传进来"
    headurl = e('_4jhq').attr('src') or e('scaledImageFitWidth').attr('src')
    dynamic_div = e("._3ccb")
    for dynamic_details in dynamic_div('.userContentWrapper'):
        spacedata = SpaceData()
        spacedata.author = author
        p = pq(dynamic_details)
        dynamic = p('._1dwg')
        # print(pq(dynamic).html())
        _e = pq(dynamic)
        title = _e('.fcg').text()
        original_or_not = '原创'
        original_content = ''
        if '分享' in title:
            original_or_not = '非原创'
            original_content = _e('._5pco').text()
        post_time = _e('.timestampContent').eq(0).text()
        content = _e('.userContent').text()
        spacedata.post_time = post_time
        spacedata.original = original_or_not
        spacedata.content = content or original_content
        print(original_or_not, '\n', post_time, content, original_content)

        item = p('.commentable_item')

        # print(pq(item).html())
        _e = pq(item)
        praise = _e('._4arz').text()
        share = _e('.UFIShareLink').text()
        comment_number = len(_e('.UFICommentBody'))
        comment_sum = comment_number
        comment_more = _e('.UFIPagerLink').text()
        if comment_more is not None:
            comment_count = re.search('\d{1,5}', comment_more)
            if comment_count is not None:
                comment_sum += int(comment_count.group())
        praise_number = (re.search('\d{1,5}', praise)).group() if (re.search('\d{1,5}', praise)) else 0
        if '席海明' in praise:
            praise_number = int(praise_number) + 1
        if '、' in praise:
            praise_number = int(praise_number) + 1
        spacedata.praise = praise_number
        spacedata.share = (re.search('\d{1,5}', share)).group() if re.search('\d{1,5}', share) else ''
        spacedata.comment_sum = comment_sum
        print(praise, share, comment_sum, '==', )

        # 获取头像，头像有多种情况
        spacedata.headurl = headurl
        spacedata.imgurl = _e('.scaledImageFitWidth').html()

        post_dict = spacedata.obj_to_dict()
        if '_id' in post_dict:
            post_dict.pop("_id")
        print("result parse_posts_html{}".format(post_dict))
        from setting import test
        test['post'].insert(post_dict)


def parse_post_person(html=''):
    # 示例 url https://www.facebook.com/pages/BigBus/103163146499275?rf=1660472990883922
    # https://www.facebook.com/pages/BigBus/103163146499275?rf=1660472990883922
    e = pq(html)
    author = "传进来"
    headurl = e('_4jhq').attr('src') or e('._4m78').find('.img').attr('src')
    dynamic_div = e("._3ccb")
    for dynamic_details in dynamic_div('.userContentWrapper'):
        spacedata = SpaceData()
        spacedata.author = author
        p = pq(dynamic_details)
        dynamic = p('._1dwg')
        # print(pq(dynamic).html())
        _e = pq(dynamic)
        title = _e('.fcg').text()
        original_or_not = '原创'
        original_content = ''
        if '分享' in title:
            original_or_not = '非原创'
            original_content = _e('._5pco').text()
        post_time = _e('.timestampContent').eq(0).text()
        content = _e('.userContent').text()
        spacedata.post_time = post_time
        spacedata.original = original_or_not
        spacedata.content = content or original_content
        print(original_or_not, '\n', post_time, content, original_content)

        # item = p('.commentable_item')

        # 获取点赞 评论
        praise_comment_str = p('._524d').text()
        praise_comment_list = praise_comment_str.split('\n') if praise_comment_str else []
        if praise_comment_list:
            for item in praise_comment_list:
                if '赞' in item:
                    spacedata.praise = item[0]
                if '评论' in item:
                    spacedata.comment_sum = item[0]
                if '转发' in item:
                    spacedata.share = item[0]

        spacedata.all_praise_comment = praise_comment_str
        # print(pq(item).html())
        # _e = pq(item)
        # praise = _e('._4arz').text()
        # share = _e('.UFIShareLink').text()
        # comment_number = len(_e('.UFICommentBody'))
        # comment_sum = comment_number
        # comment_more = _e('.UFIPagerLink').text()
        # if comment_more is not None:
        #     comment_count = re.search('\d{1,5}', comment_more)
        #     if comment_count is not None:
        #         comment_sum += int(comment_count.group())
        # praise_number = (re.search('\d{1,5}', praise)).group() if (re.search('\d{1,5}', praise)) else 0
        # if '席海明' in praise:
        #     praise_number = int(praise_number) + 1
        # if '、' in praise:
        #     praise_number = int(praise_number) + 1
        # spacedata.praise = praise_number
        # spacedata.share = (re.search('\d{1,5}', share)).group() if re.search('\d{1,5}', share) else ''
        # spacedata.comment_sum = comment_sum
        # print(praise, share, comment_sum, '==', )

        # 获取头像，头像有多种情况
        spacedata.headurl = headurl
        spacedata.imgurl = _e('.scaledImageFitWidth').html()

        post_dict = spacedata.obj_to_dict()
        if '_id' in post_dict:
            post_dict.pop("_id")
        print("result parse_posts_html{}".format(post_dict))
        from setting import test
        test['post'].insert(post_dict)

def parse_post_group(html=''):
    # 示例 url https://www.facebook.com/pages/BigBus/103163146499275?rf=1660472990883922
    # https://www.facebook.com/pages/BigBus/103163146499275?rf=1660472990883922


    e = pq(html)
    author = e('._33vv').text()
    headurl = e('._4jhq').attr('src') # or e('._4m78').find('.img').attr('src')
    dynamic_div = e("._3ccb")
    for dynamic_details in dynamic_div('.userContentWrapper'):
        spacedata = SpaceData()
        spacedata.author = author
        p = pq(dynamic_details)
        dynamic = p('._1dwg')
        # print(pq(dynamic).html())
        _e = pq(dynamic)
        # title = _e('.fcg').text()

        post_time = _e('.timestampContent').eq(0).text()
        content = _e('.userContent').text()
        spacedata.post_time = post_time
        spacedata.content = content


        item = p('.commentable_item')

        print(pq(item).html())
        _e = pq(item)
        praise = _e('.UFILikeSentenceText').text()
        share = _e('.UFIShareLink').text()
        comment_number = len(_e('.UFIComment'))

        comment_sum = comment_number
        comment_more = _e('.UFIPagerLink').text()
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

        # 获取头像，头像有多种情况
        spacedata.headurl = headurl
        imgurls = p('.uiScaledImageContainer')

        # todo 补充所有图片
        img = []
        for imgurl in imgurls:
            img.append(pq(imgurl)('.scaledImageFitHeight').attr('src'))
        spacedata.imgurl = img

        post_dict = spacedata.obj_to_dict()
        if '_id' in post_dict:
            post_dict.pop("_id")
        print("result parse_posts_html{}".format(post_dict))
        from setting import test
        test['post'].insert(post_dict)

# 种类
# inputtext (类) 需要登录  https://www.facebook.com/henry.shamsthz.5
# _2i5e 类 名字 (h1.text)  独具一类 解析  https://www.facebook.com/pages/%E8%B5%A4%E6%9F%B1759%E9%98%BF%E4%BF%A1%E5%B1%8B/139584029482895   https://www.facebook.com/pages/BigBus/103163146499275?rf=1660472990883922
# 52次赞 6条评论 可能是针对的是图片 个人 https://www.facebook.com/pages/%E8%81%96%E5%A3%AB%E6%8F%90%E5%8F%8D%E7%81%A3%E6%B3%B3%E7%81%98/143105012420920?rf=313544202035563
if __name__ == '__main__':
    driver = webdriver.Chrome()
    # url = 'https://www.facebook.com/pages/BigBus/103163146499275?rf=1660472990883922'
    # url = 'https://www.facebook.com/jumphigh.com.hk/' 群
    # url = 'https://www.facebook.com/pg/jumphigh.com.hk/posts/?ref=page_internal'
    url = 'https://www.facebook.com/pg/ivsataiwan/posts/?ref=page_internal' #群
    url = 'https://www.facebook.com/sonarband5/'
    url = 'https://www.facebook.com/pages/%E8%81%96%E5%A3%AB%E6%8F%90%E5%8F%8D%E7%81%A3%E6%B3%B3%E7%81%98/143105012420920?rf=313544202035563'  # 个人
    driver.get(url)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, '_2i5e')))

    # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, '_33vv')))
    # post_button = driver.find_element_by_class_name('_2yav')
    #
    # from selenium.webdriver.common.action_chains import ActionChains
    # ActionChains(driver).click(post_button).perform()
    # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'u_c3pyo2ta4')))
    html_init = driver.page_source
    # parse_post_person(html_init)

    #群 ._33vv 唯一标识 author
    parse_post_group(html_init)
