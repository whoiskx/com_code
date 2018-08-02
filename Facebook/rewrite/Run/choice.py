from selenium import webdriver
from pyquery import PyQuery as pq
import re


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


def person(driver):
    # 示例 url https://www.facebook.com/pages/BigBus/103163146499275?rf=1660472990883922
    # https://www.facebook.com/pages/BigBus/103163146499275?rf=1660472990883922
    # driver = webdriver.Chrome()
    # driver.get('')
    # todo 可能找不到元素 崩溃

    # 地方性商家
    author = driver.find_element_by_class_name('_2i5e').find_element_by_tag_name('h1').text

    headurl = driver.find_element_by_class_name('scaledImageFitWidth').get_attribute('src')

    post_divs = driver.find_elements_by_class_name('userContentWrapper')

    for post_details in post_divs:
        spacedata = SpaceData()
        spacedata.author = author
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

        # 获取头像，头像有多种情况
        spacedata.headurl = headurl
        # todo 一张图和多张图
        spacedata.imgurl = e('.scaledImageFitWidth').html()

        post_dict = spacedata.obj_to_dict()
        print("result parse_posts_html{}".format(post_dict))

        from setting import test
        test['post-8-2'].insert(post_dict)


def group(driver):
    return 'end'
