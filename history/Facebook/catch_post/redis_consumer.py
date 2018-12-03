import redis
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import re
driver = webdriver.Chrome()


class SpaceData(object):
    def __init__(self, author='', time='', original='', comment_sum='', share='', praise='', content=''):
        self.author = author
        self.time = time
        self.original = original
        self.comment_sum = comment_sum
        self.share = share
        self.praise = praise
        self.content = content


    def obj_to_dict(self):
        return self.__dict__


def parse_post(html):
    e = pq(html)
    dynamic_div = e("._3ccb")

    for dynamic_details in dynamic_div('.userContentWrapper'):
        spacedata = SpaceData()
        spacedata.author = e('._2i5e').find('h1').text()
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
        time = _e('.timestampContent').eq(0).text()
        content = _e('.userContent').text()
        spacedata.time = time
        spacedata.original = original_or_not
        spacedata.content = content or original_content
        print(original_or_not, '\n', time, content, original_content)

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


        post_dict = spacedata.obj_to_dict()
        if '_id' in post_dict:
            post_dict.pop("_id")
        print("result parse_posts_html{}".format(post_dict))
        from setting import test
        test['post'].insert(post_dict)


def handle(task):
    print(task)
    url = task.decode()
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, 'title')))
    time.sleep(0.5)
    # html = driver.page_source
    # name = url.split('com')[-1]
    # with open('page/{}.html'.format(name), 'w', encoding='utf-8') as f:
    #     f.write(html)
    # parse_post(html)


def main():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    while 1:
        result = r.blpop('fb_home_url', 0)
        handle(result[1])


if __name__ == "__main__":
    main()
