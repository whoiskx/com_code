import time
from pyquery import PyQuery as pq
from setting import driver_facebook, execute_times, log, urun


class PostData(object):

    def __init__(self, account_name='', time='', praise='', share='', content=''):
        self.account_name = account_name
        self.time = time
        self.praise = praise
        self.share = share
        self.content = content

    def obj_to_dict(self):
        return self.__dict__


def posts_index():
    driver = driver_facebook()
    driver.get("https://www.facebook.com/groups/southmongoliasupport//?ref=direct")
    time.sleep(4)
    execute_times(driver, 2000)
    posts_html = driver.page_source
    driver.close()

    with open("posts_index.html", "w", encoding='utf-8') as f:
        f.write(posts_html)
    log('posts_html 写入文件夹')
    return posts_html


def parse_posts_html(posts_html):
    log("begin parse_posts_html")
    e = pq(posts_html)
    results = e(".userContentWrapper")
    for count, item in enumerate(results):
        item = pq(item)
        post = PostData()
        post.account_name = item(".fwb").text()
        post.content = item(".userContent").text()
        post.time = item(".timestampContent").text().split(" ")[0]
        post.praise = item('._ipn')("._3t54").text().split("\n")[-1][:1]
        post.share = item(".UFIShareLink").text()

        if '年' in post.time:
            post.year = post.time.split("年")[0]
        else:
            post.year = 2018

        if '月' and '年' in post.time:
            post.month = post.time.split("年")[-1].split('月')[0]
        elif '月' in post.time:
            post.month = post.time.split('月')[0]

        post.day = post.time.split("月")[-1]
        post_dict = post.obj_to_dict()
        log("result parse_posts_html{}".format(post_dict))
        urun['post'].insert(post_dict)
        log('insert {} success'.format(post.account_name))


def main():
    posts_html = posts_index()
    parse_posts_html(posts_html)


if __name__ == '__main__':
    main()
