from setting import urun

db = urun.spacedata2

content_all = ''
for i in db.find():
    content_all += i.get('content')

with open('merge_result.txt', 'w', encoding='utf-8') as f:
    f.write(content_all)

print(content_all)