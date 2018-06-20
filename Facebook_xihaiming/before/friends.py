from pyquery import PyQuery as pq

with open("friends.html", 'r', encoding="utf-8") as f:
    html = f.read()

e = pq(html)
school = e("._c24 _50f4").html()

print(school)