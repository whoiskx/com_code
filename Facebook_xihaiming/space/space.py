from pyquery import PyQuery as pq
import re
from setting import driver_facebook,execute_times

# driver = driver_facebook()
# driver.get('https://www.facebook.com/profile.php?id=100023978830810')
# execute_times(driver, 3)
# html = driver.page_source
# with open('index.html', 'w', encoding='utf-8') as f:
#     f.write(html)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()


div = re.findall(r'<div class="_5pcb _4b0l">.*?<div class="_50f9 _50f3">', html)
# print(div)
e = pq(div[0])
dynamic_div = e("._3ccb")
for dynamic in dynamic_div('._1dwg'):
    # print(pq(dynamic).html())
    _e = pq(dynamic)
    title = _e('.fcg').text()
    original_or_not = '原创'
    original_content = ''
    if '分享' in title:
        original_or_not = '非原创'
        original_content = _e('._5pco').text()
    time = _e('.timestampContent').text()
    content = _e('.userContent').text()
    print(original_or_not, '\n', time, content, original_content)

# for item in dynamic_div('.commentable_item'):
#     # print(pq(item).html())
#     _e = pq(item)
#     praise = _e('._4arz').text()
#     share = _e('.UFIShareLink').text()
#     comment_number = len(_e('.UFICommentBody'))
#     comment_sum = comment_number
#     comment_more = _e('.UFIPagerLink').text()
#     if comment_more is not None:
#         comment_count = re.search('\d{1,5}', comment_more)
#         if comment_count is not None:
#             comment_sum += int(comment_count.group())
#     print(praise, share, comment_sum, '==',)
