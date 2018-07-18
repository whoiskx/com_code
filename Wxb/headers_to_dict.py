headers = """Host: www.qq.com
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: https://www.google.com/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: RK=MUIUMx6lTY; ptcz=f2b39020fd87469fd087c0b7f7e37420d38e6d332b75bde23b0e4a4b61fd0cc3; pt2gguin=o0574613576; pgv_pvid=6211376896; pgv_pvi=7068666880; o_cookie=574613576; ts_uid=6350478752; pac_uid=1_574613576; ptui_loginuin=aaafaff@qq.com; ptisp=ctc; pgv_info=ssid=s8224135895; pgv_si=s5358602240; _qpsvr_localtk=0.08829715672984895; ts_refer=www.google.com/; ad_play_index=44; qv_als=PaRAhCkPrS05VjEEA11531798051Bzwiag==; uin=o0574613576; skey=@qrTkeSXfv; tvfe_boss_uuid=19cb1313d3f0ac88"""



items = headers.split("\n")
# print(items)
d = {}
for item in items:
    k, v = item.split(": ", 1)

    d[k] = v.strip()
print(d)
