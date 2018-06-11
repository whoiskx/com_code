import string
import requests
import json
import re
import math
import hashlib
from datetime import datetime

def get_json(url):
    data = requests.get(url)
    data = json.loads(data.text)
    return data

def get_md5(string):
    md5 = hashlib.md5()
    md5.update(string.encode())
    return md5.hexdigest()

def user_handle(user):
    """处理user中的字段
    # TODO: created_at
    # FIXME: vip 字段使用默认值None
    # """
    name = user['screen_name']
    domain = user['domain'] if user.get('domain', None) else user['idstr']
    url = "http://weibo.com/{}".format(domain)
    
    location = user['location'].split(" ")
    if len(location) == 2:
        province, city = location
    else:
        province, city = location[0], ""
    headurl = user['profile_image_url']
    fans = user['followers_count']
    follows = user['friends_count']
    posts = user['statuses_count']
    favourites = user['favourites_count']

    verified_type = -1
    vip = None
    if user.get('verified') is not None:
        vip = user['verified']
        verified_type = 0
    if user.get('verified_type') is not None:
        verified_type = user['verified_type']

    verified_reason = user['verified_reason']
    description = user['description']
    sex = 1 if user['gender'] == 'm' else 2
    uid = user['idstr']
    site = 1
    tags = ""
    nature = ""
    registerTime = user['created_at']

    return {'name': name,
            'domain': domain,
            'url': url,
            'province': province,
            'city': city,
            'headurl': headurl,
            'fans': fans,
            'follows': follows,
            'posts': posts,
            'favourites': favourites,
            'verified_type': verified_type,
            'verifiedReason': verified_reason,
            'description': description,
            'sex': sex,
            'uid': uid,
            'site': site,
            'tags': tags,
            'nature': nature,
            'registerTime': registerTime,
            'vip': vip}


def geo_handle(geo):
    if geo is None:
        return ""
    else:
        x, y = geo['coordinates']
        return "{},{}".format(x, y)


def id2mid(my_id):
    mid = ''
    while True:
        if len(my_id) > 7:
            a = base62_encode(int(my_id[-7:]))
            if len(a) < 4:
                a = '0' * (4 - len(a)) + a
            mid = a + mid
            my_id = my_id[:-7]
        else:
            mid = base62_encode(int(my_id)) + mid
            break
    return mid

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def base62_encode(num, alphabet=ALPHABET):
    """10进制转62进制"""

    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def get_headurl(site, uid, url):
    if site == 3:
        url = urlencode(url)
    return "site={}&uid={}&url={}".format(site, uid, url)

def urlencode(url, codec='utf-8'):
    return url.encode(codec)

def contains(blogs, entity):
    """judge whether an entity exists"""
    for blog in blogs:
        url = blog.get('url')
        if url == entity.get('url'):
            return True
    return False

def time_format(s):
    """
    Mon Mar 12 00:33:07 +0800 2018
    """
    dt = datetime.strptime(s, "%a %b %d %H:%M:%S +0800 %Y")    
    return dt.strftime("%Y-%m-%dT%H:%M:%S+08:00")

def create_blogs(data):
    """
    data: load from response.body or response.text
    """
    results = data['statuses']
    blogs = []
    for r in results:
        # results中的每个文章的name都一样
        taskname = r['user']['screen_name']
        # GMT 时间格式字符
        # Mon Mar 12 00:33:07 +0800 2018
        create_at = r['created_at']
        # FIXME: time format
        time = time_format(create_at)
        source = re.sub("<.*?>", "", r['source'])
        
        # user 也是一个字典
        user = r.get('user')
        if user is None:
            continue
        # 处理用户字段
        user = user_handle(user)
        headUrl = user['headurl']
        uid = user['uid']
        author = user['name']
        
        content = r['text']
        geo = geo_handle(r['geo'])
        quote = ""
        qurl = ""
        quoteBlogUrl = ""
        quoteAuthorID = ""
        qid = ""
        qmid = ""
        imgurl = ""
        quid = ""
  
        quoteTime = ""

        # NOTE: strange imgurl
        if r.get('bmiddle_pic'):
            imgurl = r['bmiddle_pic']

        imgurls = r['pic_urls']
        imgCounts = len(imgurls)
        picUrls = ""
        for item in imgurls:
            picid = item['thumbnail_pic']
            picurl = picid.replace("thumbnail", "bmiddle")
            picUrls += picurl + ","
        # trim the tail ','
        picUrls = picUrls[:-1]
        
        # 处理转发quote
        quoteimgurl = ""
        quoteAuthor = ""
        qpicUrls = ""
        qimgCounts = 0
        if r.get('retweeted_status'):
            qr = r['retweeted_status']
            quser = qr['user']
            if quser:                
                quser = user_handle(quser)
                qsource = re.sub("<.*?>", "", qr['source'])
                qheadUrl = quser['headurl']
                quid = quser['uid']
                quoteAuthor = quser['name']
                quoteContent = qr['text']
                qtranstmis = qr['reposts_count']
                qcomments = qr['comments_count']
                quoteTime = time_format(qr['created_at'])
                qid = "%s" % qr['idstr']
                quote = "@{}：{}".format(quoteAuthor, quoteContent)
                qmid = id2mid(qid)
                qurl = "http://weibo.com/{}/{}".format(quid, qmid)
                
                if qr.get('bmiddle_pic'):
                    quoteimgurl = qr.get('bmiddle_pic')
                qimgurls = qr.get('pic_urls')
                qimgCounts = len(qimgurls)
                for item in qimgurls:
                    qpicid = item['thumbnail_pic']
                    qpicurl = qpicid.replace('thumbnail', 'bmiddle')
                    qpicUrls += qpicurl + ","
                # trim tailing ','
                qpicUrls = qpicUrls[:-1]

                # 建立独立的微博实体
                quoteblog = {
                    'picUrls': qpicUrls,
                    'imgCounts': qimgCounts,
                    'qimgCounts': 0,
                    'User': quser,
                    'uid': quid,
                    'quoteUid': "",
                    'author': quoteAuthor,
                    'quoteAuthor': "",
                    'content': quoteContent,
                    'quote': "",
                    'transtmis': qtranstmis,
                    'comments': qcomments,
                    'blogid': qmid,
                    'url': qurl,
                    'time': quoteTime,
                    'quoteTime': "",
                    'imageUrl': get_headurl(1, quid, qheadUrl),
                    'qurl': "",
                    # FIXME: task.site is what?
                    'authorID': get_md5('{}#{}'.format(quid, 1)),
                    'quoteAuthorID': "",
                    'imgUrl': quoteimgurl,
                    'quoteImgUrl': "",
                    'source': qsource,
                }
                quoteAuthorID = quoteblog['authorID']

                # FIXME: uncomment it
                # add to blogs:
                # if not contains(blogs, quoteblog):
                #     blogs.append(quoteblog)

        transtmis = r['reposts_count']
        comments = r['comments_count']
        attitudes_count = r['attitudes_count']
        id = "%s" % r['idstr']
        mid = id2mid(id)
        url = "http://weibo.com/{}/{}".format(uid, mid)

        blog = {
            'picUrls': picUrls,
            'imgCounts': imgCounts,
            'qpicUrls': qpicUrls,
            'qimgCounts': qimgCounts,
            'geo': geo,
            'quoteID': qmid,
            'quoteUid': quid,
            'quoteTime': quoteTime,
            'User': user,
            'uid': uid,
            'author': author,
            'content': content,
            'quote': quote,
            'transtmis': transtmis,
            'comments': comments,
            'attitudes_count': attitudes_count,
            'time': time,
            'url': url,
            'blogid': mid,
            'quoteAuthor': quoteAuthor,
            'imageUrl': get_headurl(1, uid, headUrl),
            'qurl': qurl,
            'authorID': get_md5("{}#{}".format(uid, 1)),
            'qouteAuthorID': quoteAuthorID,
            'imgUrl': imgurl,
            'quoteImgUrl': quoteimgurl,
            'source': source,
        }
        if not contains(blogs, blog):
            blogs.append(blog)
    return blogs

    

if __name__ == '__main__':
    start_url = ('https://api.weibo.com/2/statuses/user_timeline.json?'
                 'source=82966982&uid=1713926427&page=1&count=30')
    data = get_json(start_url)
    blogs = create_blogs(data)