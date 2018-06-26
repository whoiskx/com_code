from setting import urun, driver_facebook, log
from Facebook_data import FacebookData
from pyquery import PyQuery as pq
import time
from random import randint
import json
import re


error_count = 0


class PostData(FacebookData):
    # def __init__(self, account_name='', home_page='', location='', come_form='', job='', followers='', degree='',
    #              sex='', is_get=''):
    #     self.account_name = account_name
    #     self.location = location
    #     self.come_form = come_form
    #     self.job = job
    #     self.followers = followers
    #     self.degree = degree
    #     self.sex = sex
    #     self.is_get = is_get
    #     self.home_page = home_page
    #
    # def obj_to_dict(self):
    #     return self.__dict__
    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)


def personal_data(index_html):
    data_sex = re.findall(r'"addFriendText".*?<', index_html) or re.findall(
        r'<span class="FollowLink">.*?</span>',
        index_html)
    log('data_sex', data_sex)
    post = PostData()
    if len(data_sex) != 0:
        if '他' in data_sex[0]:
            post.sex = 'man'
        if "她" in data_sex[0]:
            post.sex = "woman"

    profile = re.findall(r'<div id="intro_container_id">.*?</ul></div>', index_html)
    if profile == []:
        global error_count
        error_count += 1
        log("error 第{}次, not find profile".format(error_count))

    e = pq(profile[0])
    all_profile = e.text()
    list_profile = all_profile.split("\n")
    log('list_profile', list_profile)
    for item in list_profile:
        if ("曾经" in item or '就读于' in item) and post.degree == '':
            post.degree = item
        elif "所在地" in item:
            post.location = item
        elif "来自" in item:
            post.come_form = item
        elif "粉丝" in item:
            post.followers = item
        elif "-" in item and post.job == '' and '曾经' not in item:
            post.job = item
    log('post', post)
    return post


def parse_url(url_dict):
    driver = driver_facebook()
    for count, u in enumerate(url_dict):
        # if count <= 100:
        #     continue
        try:
            link = u.get('link')
            name = u.get('name')
            log("begin name{}".format(name))
            driver.get(link)
            time.sleep(1)
            index_html = driver.page_source

            post = personal_data(index_html)

            post.account_name = name
            post.home_page = link

            urun['test'].insert(
                {
                    "account_name": post.account_name,
                    'home_page': post.home_page,
                    'location': post.location,
                    'come_form': post.come_form,
                    "job": post.job,
                    'followers': post.followers,
                    "degree": post.degree,
                    "sex": post.sex,
                    "is_get": True
                 }
            )

            log("insert {} sucessful".format(post.account_name))
            time.sleep(randint(2, 5))
            if count >= 10:
                break
        except Exception as e:
            log(count, e)
            continue


def main():
    with open("friends_url.txt", 'r', encoding="utf-8") as f:
        url_dict = json.load(f)
    # print(url_dict, type(url_dict), type(url_dict[0]), type(f))
    parse_url(url_dict)


if __name__ == '__main__':
    main()
