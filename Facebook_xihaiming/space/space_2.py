from pyquery import PyQuery as pq
import re
from setting import driver_facebook, execute_times, urun, log


class SpaceData(object):
    def __init__(self, time='', original='', comment_sum='', share='', praise='', content=''):
        self.time = time
        self.original = original
        self.comment_sum = comment_sum
        self.share = share
        self.praise = praise
        self.content = content
        self.year = ''
        self.month = ''
        self.day = ''
        self.hours = ''

    def obj_to_dict(self):
        return self.__dict__


# driver = driver_facebook()
# driver.get('https://www.facebook.com/profile.php?id=100023978830810')
# execute_times(driver, 3)
# html = driver.page_source
# with open('index.html', 'w', encoding='utf-8') as f:
#     f.write(html)

with open('posts_index22_280.html', 'r', encoding='utf-8') as f:
    html = f.read()

spacedata = SpaceData()
div = re.findall(r'<div class="_5pcb _4b0l">.*?<div class="_50f9 _50f3">', html)
# print(div)
e = pq(div[0])
dynamic_div = e("._3ccb")
for dynamic_details in dynamic_div('.userContentWrapper'):
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
    spacedata.share =  (re.search('\d{1,5}', share)).group() if re.search('\d{1,5}', share) else ''
    spacedata.comment_sum = comment_sum
    print(praise, share, comment_sum, '==', )

    if '年' in spacedata.time:
        spacedata.year = spacedata.time.split("年")[0]
    else:
        spacedata.year = 2018

    if '月' and '年' in spacedata.time:
        spacedata.month = spacedata.time.split("年")[-1].split('月')[0]
    elif '月' in spacedata.time:
        spacedata.month = spacedata.time.split('月')[0]
    elif '月' not in spacedata.time:
        spacedata.month = '6'

    if '日' in spacedata.time:
        spacedata.day = spacedata.time.split('日')[0]
        if '月' in spacedata.day:
            spacedata.day = spacedata.day.split('月')[1]
    elif '昨天' in spacedata.time:
        spacedata.day = '28'
    elif '小时' in spacedata.time:
        spacedata.day = '29'

    if '上午' in spacedata.time:
        hour_raw = spacedata.time.split('午')[1]
        spacedata.hours = hour_raw.split(':')[0]
    if '下午' in spacedata.time:
        hour_raw = spacedata.time.split('午')[1]
        spacedata.hours = int(hour_raw.split(':')[0]) + 12

    if '小时' in spacedata.time:
        spacedata.hours = spacedata.time.split('小')[0] + '小时前'  # 当前时间 （9:00)
        spacedata.day = '29'
        spacedata.month = '6'
        spacedata.year = '2018'

    if '分钟' in spacedata.time:
        spacedata.day = '29'
        spacedata.month = '6'
        spacedata.year = '2018'

    post_dict = spacedata.obj_to_dict()
    if '_id' in post_dict:
        post_dict.pop("_id")
    log("result parse_posts_html{}".format(post_dict))
    urun['spacedata280'].insert(post_dict)
