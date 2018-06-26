import time
from pyquery import PyQuery as pq
from setting import driver_facebook, execute_times, log, urun
import re
from Facebook_data import FacebookData


class MembersData(FacebookData):
    def __init__(self):
        super(MembersData, self).__init__()


def members_html(url):
    driver = driver_facebook()
    driver.get(url)
    execute_times(driver, 10)
    html = driver.page_source
    # with open("group_members.html", "w", encoding="utf-8") as f:
    #     f.write(html)
    log(html)
    driver.close()
    return html


def members_url(html):
    group_members_div = re.findall(r'<div id="groupsMemberBrowser".*?<div id="bottomContent"></div>', html)
    if group_members_div == []:
        print("not find group_members_div")
        return {}
    e = pq(group_members_div[0])
    # print(e('_6a'))
    # e('._6a')('.fsl').find('a').attr('href')

    all_members_div = e('._6a')('.fsl')
    results = []
    for member in all_members_div:
        members_url = pq(member).find('a').attr('href')
        name = pq(member).find('a').text()
        results.append({"name": name, 'url': members_url})

    # print(results)
    print(len(results))
    # import json
    #
    # s = json.dumps(results, indent=2, ensure_ascii=False)
    # with open('members_url.txt', 'w', encoding='utf-8') as f:
    #     f.write(s)
    return results


def parse_members_url(url_dict):
    driver = driver_facebook()
    error_count = 0
    for count, u in enumerate(url_dict):
        if count <= 10:
            log("skip {} {}".format(count, u.get('name')))
            continue
        link = u.get('url')
        name = u.get('name')
        log("begin {} : {}", count, name)
        try:
            driver.get(link)
            time.sleep(2)
            post = MembersData()
            index_html = driver.page_source
            data_sex = re.findall(r'"addFriendText".*?<', index_html) or re.findall(
                r'<span class="FollowLink">.*?</span>',
                index_html)
            log(data_sex)
            if data_sex != []:
                if '他' in data_sex[0]:
                    post.sex = 'man'
                if "她" in data_sex[0]:
                    post.sex = "woman"

            profile = re.findall(r'<div id="intro_container_id">.*?</ul></div>', index_html)
            if profile == []:
                error_count += 1
                log("error {} : {} {}".format(error_count, count, link))
            e = pq(profile[0])
            all_profile = e.text()
            log(all_profile)
            list_profile = all_profile.split("\n")

            for item in list_profile:
                if ("曾经" in item or '就读于' in item) and post.degree == '':
                    post.degree = item
                elif "所在地" in item:
                    post.location = item
                elif "来自" in item:
                    post.come_form = item
                elif "粉丝" in item:
                    post.followers = item
                elif "-" in item and post.job == '':
                    post.job = item

            post.account_name = name
            post.home_page = link
            log("post", post)
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
            log("insert {} sucessful".format(name))
            if count >= 700:
                break
        except Exception as e:
            log(count, name, e)
            continue


def main():
    url = "https://www.facebook.com/groups/southmongoliasupport/members/"
    html = members_html(url)
    members_url_dict = members_url(html)
    parse_members_url(members_url_dict)


if __name__ == '__main__':
    main()
