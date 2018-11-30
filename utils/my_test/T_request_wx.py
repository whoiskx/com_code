import requests

url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MTI2MTI0MA==&scene=124&uin=MTE1NjkxODg2MQ%3D%3D&key=8fe127ee65c542467049c30ff4271d018867b9cbec8b49c052ba308a3443811a6a98d2c7a6af37e0a4760c1972cc07b405d07b958a8954b92bec4a77bb3c15a3cd353da93fdd026bd74153b01755a851&devicetype=Windows+10&version=6206034e&lang=zh_CN&a8scene=7&pass_ticket=Efb2GurPHFS4qNJUKPCFd9OHejaYHx4PS48kgFwyYYnH2r%2FjBqOSXH%2BE%2BS3BFsGv&winzoom=1"
url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MTI2MTI0MA==&scene=124&uin=MTE1NjkxODg2MQ%3D%3D&key=8fe127ee65c542467049c30ff4271d018867b9cbec8b49c052ba308a3443811a6a98d2c7a6af37e0a4760c1972cc07b405d07b958a8954b92bec4a77bb3c15a3cd353da93fdd026bd74153b01755a851&devicetype=Windows+10&version=6206034e&lang=zh_CN&a8scene=7&pass_ticket=Efb2GurPHFS4qNJUKPCFd9OHejaYHx4PS48kgFwyYYnH2r%2FjBqOSXH%2BE%2BS3BFsGv&winzoom=1"
url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MTI2MTI0MA==&scene=124&uin=MTE1NjkxODg2MQ%3D%3D&key=8bc582cd83ca114ff4f5690c68ea267d6be3e9a3794c0e569bee9438fcddb94ae81b7aeca0c27e3d9ea7a23c6a397d62f9938effe8fd622c786abb0e4de2eab9fe0d5c282912c21d678bc2e12defa36c&devicetype=Windows+10&version=6206034e&lang=zh_CN&a8scene=7&pass_ticket=Efb2GurPHFS4qNJUKPCFd9OHejaYHx4PS48kgFwyYYnH2r%2FjBqOSXH%2BE%2BS3BFsGv&winzoom=1"

# 寻找 阅读数跟 点赞数
url = 'https://mp.weixin.qq.com/s?__biz=MjM5MTI2MTI0MA==&mid=2655142384&idx=5&sn=0a46bb000ec935f88648852f1774ad1f&chksm=bd0ed6a78a795fb1d71ae72d99898c0f3236f3dce5775aeef95d52f1989e8dcf311118ea3f1a&scene=38&key=9971a8088dcd256b3c5f9e114c5b8ea19ce564193940ca89630f7d9d6553b25eebbd5ccd0a5493f97e6f85a547656ab071fe0f891d2cea44ccfde90d63d4d0d47b23e487dc8466a844c71b6d7aabb80f&ascene=7&uin=MTE1NjkxODg2MQ%3D%3D&devicetype=Windows+10&version=6206034e&lang=zh_CN&pass_ticket=3%2FYWynnjmDdVMJ1aK%2B2ZV8m%2F4ak0HoJiaEIQwjsp2YPFfbQYwBbp1Yn%2B38FbNU13&winzoom=1%22,%20%22webSocketDebuggerUrl%22:%20%22ws://127.0.0.1:9222/devtools/page/DF35081D-C405-4591-AB1E-5492EFBFBBCF'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; HM NOTE 1LTEW Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Ver'
#     'sion/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 MicroMessenger/6. 0.0.54r849063.501 NetType/WIFI'
#     }

resp = requests.get(url)
resp.encoding = 'utf-8'
print(resp.text)
with open('wx.html', 'w', encoding='utf-8') as f:
    f.write(resp.text)
# print(resp.text)