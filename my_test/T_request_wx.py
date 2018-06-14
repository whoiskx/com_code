import requests

url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MTI2MTI0MA==&scene=124&uin=MTE1NjkxODg2MQ%3D%3D&key=8fe127ee65c542467049c30ff4271d018867b9cbec8b49c052ba308a3443811a6a98d2c7a6af37e0a4760c1972cc07b405d07b958a8954b92bec4a77bb3c15a3cd353da93fdd026bd74153b01755a851&devicetype=Windows+10&version=6206034e&lang=zh_CN&a8scene=7&pass_ticket=Efb2GurPHFS4qNJUKPCFd9OHejaYHx4PS48kgFwyYYnH2r%2FjBqOSXH%2BE%2BS3BFsGv&winzoom=1"
url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MTI2MTI0MA==&scene=124&uin=MTE1NjkxODg2MQ%3D%3D&key=8fe127ee65c542467049c30ff4271d018867b9cbec8b49c052ba308a3443811a6a98d2c7a6af37e0a4760c1972cc07b405d07b958a8954b92bec4a77bb3c15a3cd353da93fdd026bd74153b01755a851&devicetype=Windows+10&version=6206034e&lang=zh_CN&a8scene=7&pass_ticket=Efb2GurPHFS4qNJUKPCFd9OHejaYHx4PS48kgFwyYYnH2r%2FjBqOSXH%2BE%2BS3BFsGv&winzoom=1"
url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MTI2MTI0MA==&scene=124&uin=MTE1NjkxODg2MQ%3D%3D&key=8bc582cd83ca114ff4f5690c68ea267d6be3e9a3794c0e569bee9438fcddb94ae81b7aeca0c27e3d9ea7a23c6a397d62f9938effe8fd622c786abb0e4de2eab9fe0d5c282912c21d678bc2e12defa36c&devicetype=Windows+10&version=6206034e&lang=zh_CN&a8scene=7&pass_ticket=Efb2GurPHFS4qNJUKPCFd9OHejaYHx4PS48kgFwyYYnH2r%2FjBqOSXH%2BE%2BS3BFsGv&winzoom=1"
headers = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0',
    # 'Connection': 'keep-alive',
    # 'Cookie': 'RK=MUIUMx6lTY; ptcz=f2b39020fd87469fd087c0b7f7e37420d38e6d332b75bde23b0e4a4b61fd0cc3; pt2gguin=o0574613576; pgv_pvid=6211376896; ua_id=c4frKJ6bo64FTXz4AAAAAOG1AJrMtg4x9sLPisUvdJ0=; mm_lang=zh_CN; pgv_pvi=7068666880; pgv_si=s4474253312; pgv_info=ssid=s5843357633; wxuin=1156918861; devicetype=Windows10; version=6206034e; lang=zh_CN; pass_ticket=Efb2GurPHFS4qNJUKPCFd9OHejaYHx4PS48kgFwyYYnH2r/jBqOSXH+E+S3BFsGv; rewardsn=; wxtokenkey=777; wap_sid2=CM3c1KcEElxRdUlZSndiMDh6R25LVjNoWFVyS1lHNTBWTUllZHFESGxGQ2FDbUhqM3p0bmU3UmtyeE5FUVo3aHZueE90alF2Y3lpLW9fVjQtOFluVnhkcTNXY1lUTUFEQUFBfjCDzoLZBTgNQJVO',
    # 'Host': 'mp.weixin.qq.com', 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; HM NOTE 1LTEW Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Ver'
    'sion/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 MicroMessenger/6. 0.0.54r849063.501 NetType/WIFI'
    # 'User-Agent': "Mozilla/5.0 (Linux; Android 8.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044103 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060737) NetType/WIFI Language/zh_CN"
    }

resp = requests.get(url, headers=headers)
print(resp.text)