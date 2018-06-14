
headers = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: max-age=0
Connection: keep-alive
Cookie: RK=MUIUMx6lTY; ptcz=f2b39020fd87469fd087c0b7f7e37420d38e6d332b75bde23b0e4a4b61fd0cc3; pt2gguin=o0574613576; pgv_pvid=6211376896; ua_id=c4frKJ6bo64FTXz4AAAAAOG1AJrMtg4x9sLPisUvdJ0=; mm_lang=zh_CN; pgv_pvi=7068666880; pgv_si=s4474253312; pgv_info=ssid=s5843357633; wxuin=1156918861; devicetype=Windows10; version=6206034e; lang=zh_CN; pass_ticket=Efb2GurPHFS4qNJUKPCFd9OHejaYHx4PS48kgFwyYYnH2r/jBqOSXH+E+S3BFsGv; rewardsn=; wxtokenkey=777; wap_sid2=CM3c1KcEElxRdUlZSndiMDh6R25LVjNoWFVyS1lHNTBWTUllZHFESGxGQ2FDbUhqM3p0bmU3UmtyeE5FUVo3aHZueE90alF2Y3lpLW9fVjQtOFluVnhkcTNXY1lUTUFEQUFBfjCDzoLZBTgNQJVO
Host: mp.weixin.qq.com
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Linux; Android 4.4.4; HM NOTE 1LTEW Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 MicroMessenger/6. 0.0.54_r849063.501 NetType/WIFI"""

items = headers.split("\n")
d = {}
for item in items:
    k, v = item.split(":", 1)
    d[k] = v.strip()
print(d)