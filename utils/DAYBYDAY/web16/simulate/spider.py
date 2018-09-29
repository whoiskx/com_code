import os
import requests
from pyquery import PyQuery as pq
'''
1. 抓包工具
    1.1 协议层
        1.1.1 tcp 传奇外挂 解包工具 抓包工具 wireshark
        1.1.2 udp
        1.1.3 http fiddler
    1.2 作用
        1. 分别前后端 谁的问题
        2. 学习目的
        3. 限速 代理 -> pc网络 fiddler
    1.3 https本身安全 证书 中间人
2. 爬虫
    1. 用途 搜索引擎 query -> page rank spider -> page
    2. 数据分析 量化分析
    3. 种类
        3.1 裸请求
        3.2 反爬虫 ua 限制
        3.3 SPA js代码 -> webkit
    4. robots.txt
    5. 做法
        1. 可变不可变分离
        2. 业务拆分解耦

        1. Downloader 下载器        requests(urllib2 urllib urllib3)
        2. html页面 -> 结构化的页面 Html Parser  pyquery(lxml)
        3. DataModel

        1. io复用 select poll epoll/kqueue asyncore.py
        2. 消息队列
            download -> queue
            parser ->queue -> datamodel

            celery
            sinatra

            RabbitMQ

3.x 编码
    数字 字符串 类型实例 - 二进制
    字符串 - 二进制 （编码）
    unicode - utf8 utf16 utf32

    字符串 -> encode() -> 二进制
    二进制 -> decode(utf8) -> 字符串

    终端
    file
    editor

3. json RESTful 分摊负载
    json -> 服务器渲染
            SPA 客户端渲染 ajax -> 数据 -> 最后去生成页面
            json 1. 跨框架 2. 跨语言
            ajax -> json -> 生成数据改变页面

    RESTful api url就是资源，就是访问资源形式。
    GET    /users
    GET    /user/1
    PATCH  /users
    PUT    /users
    DELETE /user/1
    GET    /user/1/items
    GET    /user/1/item/1

    restful
    rpc
'''


class Model(object):
    """
    基类, 用来显示类的信息
    """
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Movie(Model):
    """
    存储电影信息
    """
    def __init__(self):
        self.name = ''
        self.score = 0
        self.quote = ''
        self.cover_url = ''
        self.ranking = 0


def cached_url(url):
    """
    缓存, 避免重复下载网页浪费时间
    """

    '''
    cdn
    分布式redis
    nginx
    内存
    '''
    folder = 'cached'
    filename = url.split('=', 1)[-1] + '.html'
    #'cached/0.html'
    path = os.path.join(folder, filename)
    # 1. 如果我有
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 建立 cached 文件夹
        if not os.path.exists(folder):
            os.makedirs(folder)

        headers = {
            'user-agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
        }
        # 发送网络请求, 把结果写入到文件夹中
        r = requests.get(url, headers)
        with open(path, 'wb') as f:
            f.write(r.content)
        return r.content


def movie_from_div(div):
    """
    从一个 div 里面获取到一个电影信息
    """
    e = pq(div)

    # 小作用域变量用单字符
    m = Movie()
    m.name = e('.title').text()
    m.score = e('.rating_num').text()
    m.quote = e('.inq').text()
    m.cover_url = e('img').attr('src')
    m.ranking = e('.pic').find('em').text()

    return m


def movies_from_url(url):
    """
    从 url 中下载网页并解析出页面内所有的电影
    """

    # 1. 得到一个页面
    page = cached_url(url)

    # 2. 页面生成结构化的dom -> element tree
    e = pq(page)
    # print(page.decode())

    # . #
    items = e('.item')
    # 调用 movie_from_div
    # list comprehension
    # 这里生成了所有的movie
    movies = [movie_from_div(i) for i in items]
    return movies


def download_image(url):
    folder = "img"
    name = url.split("/")[-1]
    path = os.path.join(folder, name)

    if not os.path.exists(folder):
        os.makedirs(folder)

    if os.path.exists(path):
        return

    headers = {
        'user-agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
    }
    # 发送网络请求, 把结果写入到文件夹中
    r = requests.get(url, headers)
    with open(path, 'wb') as f:
        f.write(r.content)


def main():
    # 抓10个网页 包含所有的250个电影信息
    for i in range(0, 250, 25):
        # https://movie.douban.com/top250?start=0
        # https://movie.douban.com/top250?start=25
        # https: // movie.douban.com/top250?start = 225
        url = 'https://movie.douban.com/top250?start={}'.format(i)
        movies = movies_from_url(url)
        print('top250 movies', movies)
        #[download_image(m.cover_url) for m in movies]


if __name__ == '__main__':
    main()
