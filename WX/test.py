import urllib.parse

# str_result = "%25E5%25A4%25A7%25E9%2587%258D%25E7%2582%25B9%25E9%25A1%25B9%25E7%259B%25AE%25E6%259B%259D%25E5%2585%2589%25EF%25BC%2581%25E4%25BD%259B%25E5%25B1%25B1%25E4%25B8%2589%25E6%2597%25A7%25E6%2594%25B9%25E9%2580%25A0%25E5%25AE%25A3%25E4%25BC%25A0%25E5%25A4%25A7%25E7%2589%2587%25E5%2587%25BA%25E7%2582%2589"
# str_result = '%25E5%25BC%25A0%25E6%25A7%258E%25E4%25B8%25AD%25E5%25BF%2583%25E6%259E%25A2%25E7%25BA%25BD%25E7%25AB%2599%25E5%25BC%2580%25E6%258C%2582%25E4%25BA%2586%25EF%25BC%259A1%25E6%259D%25A1%25E5%259F%258E%25E8%25BD%25A8%252B5%25E6%259D%25A1%25E5%259C%25B0%25E9%2593%2581%25E4%25BA%25A4%25E6%25B1%2587%25EF%25BC%2581%25E5%2591%25A8%25E8%25BE%25B9%25E6%2588%25BF%25E4%25BB%25B7%25E8%25BF%2598%25E6%2598%25AF%25E4%25B8%2587%25E5%2585%2583%25E8%25B5%25B7%25E6%25AD%25A5...'
# str_result = urllib.parse.unquote(str_result, encoding='utf-8')
# print(str_result)
# s = urllib.parse.unquote(str_result, encoding='utf-8')
# print(s)

# 编码
raw_title = '注意 | 暴雨已发货！江苏这些地方请注意查收！'

first_encode = urllib.parse.quote(raw_title, encoding='utf-8')
print('first', first_encode)
endcode_result = urllib.parse.quote(first_encode, encoding='utf-8')
print('second', endcode_result)

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