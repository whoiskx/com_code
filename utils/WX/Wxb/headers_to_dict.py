headers = """Host: www.facebook.com
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
Accept: */*
Referer: https://www.facebook.com/kaifulee/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: datr=OxkjW4MYaIelucIws97V02xW; sb=_R0jWyoRctx7GnDrlLyCjFE2; locale=zh_CN; reg_fb_gate=https%3A%2F%2Fwww.facebook.com%2F%3Fstype%3Dlo%26jlou%3DAfdmrme287GtQ8lDAYck8Hr1EdS4sblomJegt_cx_mNGnKKQO8KxWztiQLmh6lcwzVEu-tx2eWAUqsb3p3xRDLA6Cq6PAIhCF7sRsBm6B_N-XQ%26smuh%3D17460%26lh%3DAc-qSkVMZrAqy38q; reg_fb_ref=https%3A%2F%2Fwww.facebook.com%2F%3Fstype%3Dlo%26jlou%3DAfdmrme287GtQ8lDAYck8Hr1EdS4sblomJegt_cx_mNGnKKQO8KxWztiQLmh6lcwzVEu-tx2eWAUqsb3p3xRDLA6Cq6PAIhCF7sRsBm6B_N-XQ%26smuh%3D17460%26lh%3DAc-qSkVMZrAqy38q; fr=0ICeTuNMbW3ThPfuj.AWWZ32_QLPFYehoSyw0JOzFUdOA.BbHxb1.s-.AAA.0.0.BbVTf9.AWU-qwyh; wd=1920x946"""


items = headers.split("\n")
# print(items)
d = {}
for item in items:
    k, v = item.split(": ", 1)

    d[k] = v.strip()
print(d)
