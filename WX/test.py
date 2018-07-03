
str_result = "%25E5%25A4%25A7%25E9%2587%258D%25E7%2582%25B9%25E9%25A1%25B9%25E7%259B%25AE%25E6%259B%259D%25E5%2585%2589%25EF%25BC%2581%25E4%25BD%259B%25E5%25B1%25B1%25E4%25B8%2589%25E6%2597%25A7%25E6%2594%25B9%25E9%2580%25A0%25E5%25AE%25A3%25E4%25BC%25A0%25E5%25A4%25A7%25E7%2589%2587%25E5%2587%25BA%25E7%2582%2589"
import urllib.parse
# str_result = urllib.parse.unquote(str_result, encoding='utf-8')
print(str_result)
# s = urllib.parse.unquote(str_result, encoding='utf-8')
# print(s)

# 编码
raw_title = '大重点项目曝光！佛山三旧改造宣传大片出炉'

first_encode = urllib.parse.quote(raw_title, encoding='utf-8')

endcode_result = urllib.parse.quote(first_encode, encoding='utf-8')
print(endcode_result)
