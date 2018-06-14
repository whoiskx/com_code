import re

with open('Response.txt', "r", encoding='utf-8',errors='ignore') as f:
    mylist = "".join(f.readlines()[:])
    row_article_list = mylist.replace('\t', '').replace(' ', '').replace('&quot;', '').replace('&nbsp;', '').replace(
        '\\\\', '').replace('amp;amp;', '').replace(',', '')
    result = re.findall("p.weixin.qq.co", row_article_list)

    print(row_article_list)

    print(result)
