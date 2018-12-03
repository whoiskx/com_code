html = '<h1><em>赤柱監獄</em></h1>'
from pyquery import PyQuery as pq

e = pq(html)
print(e.find('h1'))

m = '<p item="name"><span><em>Whoah!</em></span></p><p><em> there</em></p>'
d = pq(m)
print(d.find('p'))

print(d('p').eq(1).find('em'))
