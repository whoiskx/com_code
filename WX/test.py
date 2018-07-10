import urllib.parse

# str_result = "%25E5%25A4%25A7%25E9%2587%258D%25E7%2582%25B9%25E9%25A1%25B9%25E7%259B%25AE%25E6%259B%259D%25E5%2585%2589%25EF%25BC%2581%25E4%25BD%259B%25E5%25B1%25B1%25E4%25B8%2589%25E6%2597%25A7%25E6%2594%25B9%25E9%2580%25A0%25E5%25AE%25A3%25E4%25BC%25A0%25E5%25A4%25A7%25E7%2589%2587%25E5%2587%25BA%25E7%2582%2589"
str_result = '%E2%80%A6'
str_result = 'HEY%25EF%25BC%258C%25E8%25BF%2599%25E6%259D%25AF%25E5%2586%25B0%25E7%25BE%258E%25E5%25BC%258F%25E6%259C%2589%25E7%2582%25B9%25E6%25BD%25AE%25EF%25BC%2581%25E4%25BD%25A0%25E5%2596%259D%25E8%25BF%2587%25E5%2590%2597%25EF%25BC%259F'
str_result = urllib.parse.unquote(str_result, encoding='utf-8')
print(str_result)
s = urllib.parse.unquote(str_result, encoding='utf-8')
print(s)

# 编码
# raw_title = '注意 | 暴雨已发货！江苏这些地方请注意查收！'
#
# first_encode = urllib.parse.quote(raw_title, encoding='utf-8')
# print('first', first_encode)
# endcode_result = urllib.parse.quote(first_encode, encoding='utf-8')
# print('second', endcode_result)

#
# with open('resp.txt', 'r', encoding='utf-8') as f:
#     resp = f.read()
#
#     # import json
#     # r = json.load(f)
#     # print(r, type(r))
#
# import json
# r = json.loads(resp)
# print(r, type(r))
#
# appmsgstat = r.get('appmsgstat')
# print(appmsgstat.get("read_num"))
# print(appmsgstat.get("like_num"))