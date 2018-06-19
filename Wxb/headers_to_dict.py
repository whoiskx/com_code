
headers = """Host: graph.facebook.com
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: datr=OxkjW4MYaIelucIws97V02xW; wd=1920x946; sb=_R0jWyoRctx7GnDrlLyCjFE2; c_user=100005036989194; xs=32%3Am5RP8dyGJGCEZg%3A2%3A1529028093%3A-1%3A-1; pl=n; fr=0ICeTuNMbW3ThPfuj.AWW3O-4qdU12Mkzlc15GCq9APr4.BbHxb1.s-.Fsj.0.0.BbIx39.; act=1529028586747%2F2"""
items = headers.split("\n")
print(items)
d = {}
for item in items:
    k, v = item.split(": ", 1)

    d[k] = v.strip()
print(d)