from pyquery import PyQuery as pq

# doc = pq(filename="pyquery_example.html")
#
# x = doc(".item-0")
# # print(x("td"))
# # print(doc.html())
# data = doc('tr')
# for tr in data.items():# 遍历 data 中的 <tr> 元素
#     temp = tr('td').eq(1).text() # 选取第3个 <td> 元素中的文本块
# print(temp)

# p=pq("<head><title>Hello World!</title></head>")
#
# print(p('title').html())# 获取相应的 HTML 块)
# print(p('head').text())# 获取相应)


d = pq("<div><p id='item-0'>test 1</p><p class='item-1'>test 2</p></div>")

print(d('div').html())# 获取 <div> 元素内的 HTML 块
print(d('#item-0'))# 获取 id 为 item-0 的元素内的文本内容
print(d('.item-1').text())# 获取 class 为 item-1 的元素的文本内容
#
# d = pq("<div><p id='item-0'>test 1</p><p class='item-1'>test 2</p></div>")
# y = d('p')
#
# print(type(y), y)# 获取第二个 p 元素的文本内容，

# d = pq("<div><p id='item-0'>test 1</p><p class='item-1'>test 2</p></div>")
# x = d('div').find('p')
# print(type(x), x)
# print(d('div').find('p'))# 查找 <div> 内的 p 元素
# print(d('div').find('p').eq(0))
#
# d = pq("<div><p id='item-0'>test 1</p><p class='item-1'>test 2</p></div>")
#
# # print(d('p').filter('.item-1')) # 查找 class 为 item-1 的 p 元素
# print(d('div').find('p')) # 查找 id 为 item-0 的 p 元素
