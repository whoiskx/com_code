from pyquery import PyQuery as pq
from setting import urun

with open('post_490.html', 'r', encoding='utf-8') as f:
    html = f.read()


class PostData(object):
    def __init__(self, name='', time='', praise='', share='', content=''):
        self.name = name
        self.time = time
        self.praise = praise
        self.share = share
        self.content = content

    def obj_to_dict(self):
        return self.__dict__


e = pq(html)
# 解析 赞同
# praise = e('._ipn')
# # print(1)
# # print(praise)
#
# for i in praise:
#     d = pq(i)
#     print("**{} :: ".format(d("._3t54").text().split("\n")[0]))
#
# UFIShareLink
results = e(".userContentWrapper")
for count, item in enumerate(results):
    item = pq(item)
    post = PostData()
    post.name = item(".fwb").text()
    post.content = item(".userContent").text()
    post.time = item(".timestampContent").text().split(" ")[0]
    post.praise = item('._ipn')("._3t54").text().split("\n")[-1][:1]
    post.share = item(".UFIShareLink").text()
    # print(item(".fwb").text())
    # print(item(".timestampContent").text().split(" ")[0])
    # print(item(".userContent").text())
    # print("********")
    # print(item('._ipn')("._3t54").text().split("\n")[-1])
    # print(item(".UFIShareLink").text())
    # print('====')
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
    print(post_dict)
    urun['post_year'].insert(post_dict)
