import redis
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import re

with open('temp.html', 'r', encoding='utf-8') as f:
    html_init = f.read()


class SpaceData(object):
    def __init__(self, author='', post_time='', original='', comment_sum='', share='', praise='', content='',
                 imgurl=''):
        self.author = author
        self.post_time = post_time
        self.original = original
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


if __name__ == '__main__':
    driver = webdriver.Chrome()
    url = 'https://www.facebook.com/pages/BigBus/103163146499275?rf=1660472990883922'
    driver.get(url)
    html_init = driver.page_source
    parse_post_person(html_init)
