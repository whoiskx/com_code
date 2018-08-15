# encoding=utf-8
import json

import requests

body_one = [{'headers': {'topic': 'weixin', 'key': '11709b44801b75a99898d202160e7a06', 'timestamp': 1534301212},
            'body': json.dumps({'ID': '11709b44801b75a99898d202160e7a06', 'Account': 'smzdc2015', 'TaskID': '59508952',
                     'TaskName': '微信_什么值得吃', 'AccountID': '59508952', 'SiteID': 59508952, 'TopicID': 0,
                     'Url': 'http://mp.weixin.qq.com/s?__biz=MjM5NzI5ODE3Nw==&mid=2655272443&idx=2&sn=daac55027109d67ab64416a6fe3a8b21&chksm=bd6cb4958a1b3d83cffba55fa5d49d88d616cbc27a080cd86a5d5657b5f72a958e6ecedc3ec4&scene=27#wechat_redirect',
                     'Title': 'dafafa',
                     'Content': 'safafd',
                                   # '夏天的进度条已经过半了，转眼又到了下半年，这意味着马上就要过七夕节、国庆节、圣诞节、元旦节……啦，一想到可以出门撒欢浪就超级开心。今天我们的好朋友「日和手帖」为大家搜罗了超多好玩的展，还不知道假期要去哪里玩？一起来看看吧！本文已获授权，内容转载自公众号：日和手帖 ID:hiyori_techo▼微型模型达人田中达也在台中开启奇想世界；西班牙黑色幽默画家 Joan Cornellà 作品再抵台，带你掉进荒谬世界里！Hermès将大型游乐间降落巴黎第八区；美国著名空间设计团队SNARKITECTURE，举行香港首个互动艺术装置企划；1500只比卡丘在横滨大游行？本周，日和手帖为你精选的全球最新奇有趣的展览，在这里~👇①田中达也的奇想世界·台中有丰富幽默感和想像力的微型模型达人——田中达也，擅长利用自己收藏的微型玩偶加上日常熟悉的物品来构建场景，并透过高超的技巧拍摄出一个个幽默、有趣又富含寓意的「迷你疗愈世界」！他的IG追踪人数达132万，也创立了微型日历，概念是“只要有心，每天都可以在生活中探索新发现"。厉害的是他每天发表微型模型创作，至今已维持7年时间。从即日起至9月9日，田中达也的作品会在台中展出与大家见面。此次「田中达也的奇想世界」台中站共有9大专区、39件实体作品、151件摄影作品。田中大师还会亲自为台中设计3件隐藏作品。展内精致微型人偶和巨大装置艺术都超好拍。INFORMATION台中 - 微型展－田中达也的奇想世界地址： 台中市西屯区天保街60号 (台中世贸中心)开放时间： 即日起至2018/09/09 10:00-18:00②Joan Cornellà 暗黑病态漫画登陆台北曾在2016年首度访台，短短17天吸引超过2万人朝圣的西班牙黑色幽默怪才Joan Cornellà，今年9月即将与「JUSTLIVE 就是现场」合作举办《Joan Cornellà: A Taipei Solo Exhibition 台北特展2018》。这次的展期时间更长，将带来更多的全新画作及雕塑，挑战更诡谲、暴力的超敏感话题。 Joan Cornellà 更放话，展览期间将会不定期突击展场，让观众一起体验超限制级的疯狂世界！出生于巴赛隆纳的Joan Cornellà ，他的笔下画作经常被认为令人恐怖不安，或者完全无视世俗规条，以简单视觉语言与讽刺手法，通过无数非现实情景，诠释邪恶事物或者人性阴暗面，可谓纵情于荒诞及不道德当中。笔下人物总在不对的时候露出灿笑，看了就让人不寒而栗。如果你计划去看 Joan Cornellà 的展览，不要多想，就任头脑徜徉在 Joan Cornellà 那既失真却又真实到可怕的世界吧。INFORMATION日期：2018年9月7日至30日（逢星期一休展）时间：上午11点至下午7点场地：Woolloomooloo Xhibit地址：台北市信义区信义路4段385号5楼③Hermès将大型游乐间降落巴黎第八区「难道玩乐本身，不是构成乌托邦轮廓的主要元素吗？」今年，Hermès的艺术执导Pierre-Alexis Dumas这么对所有人提问。一向以动态、自由又充满创意闻名世界的经典高端品牌Hermès，确实很适合在这个人们经常过度认真的时代之中如此主张，纵使今年已经迎来创立第181 个年头，Hermès从未舍弃他们对时尚的玩心。这一次，Hermès为许久没有爬上溜滑梯的大人们在巴黎第八区的 Hôtel Salomon de Rothschild 打造了一座大型「游乐间 (Play House)」，并要求所有宾客：「请过度盛装出席！」在这个恍如《爱丽丝梦游仙境》一般超现实又充满童话魅力的展览之中，受邀的宾客在两层楼的空间尽情于玩家、演员、宾客三种角色之间切换。在俄罗斯轮盘、赌场百家乐桌前，与会的人们能成为有趣游戏的玩家；而在舞台之上，配合着不同的场布与戏服，人们更能化身演员切换各种不同角色；至于充满超现实氛围的展间，则让宾客享受展览带来的丰富想像力。④海港城 × SNARKITECTURE彈彈球「大球場」这个夏天，来到海港城，就能置身一堆白色弹弹球中！海港城×美国著名空间设计团队SNARKITECTURE，即日至9月2日举行香港首个互动艺术装置企划 ——「BOUNCE」。他们在海港城兴建了一个超大型的互动「大球场」，打破艺术与建筑间的框架，把弹弹球放大300倍。大家可在这独特构建的空间内自由滚动、高举和投掷巨型白色充气弹弹波，无论大人小朋友都可参与其中齐齐玩乐。游人可在白色钢框架组成的龙门阵内随意耍玩过百个直径一米的白色巨型弹弹球。大家亦可到「海港城‧美术馆」参观巨型波波阵装置艺术，白色与银色巨型弹弹球填满美术馆，配以一条大型滚轴，让巨型弹弹波于轨道上滑行，融入巨型弹弹波秘密空间。INFORMATION海港城 × SNARKITECTURE 「BOUNCE」互动「大球场」日期：即日至2018年9月2日时间：上午11时至晚上7时30分 (逢正点、30分开始)地点：海港城海运大厦露天广场⑤大量比卡丘正在横滨游行ing！每年暑假在日本横滨举行的活动「比卡丘大量发生中」，今年已经到了第5届，本次还集合了1500只比卡丘成堆卖萌！其中例行的Super Soaking Splash Show，让这酷热的暑假凉凉的~还有携带大量皮卡丘的船将出现在Minato Mirai的海洋中！据说今年的比卡丘们会以新装扮出场。官方也已宣布了今年会首度加入伊布游行，由于和比卡丘游行的时间和地点是错开的，大家无缘看到20：20对打画面了。INFORMATIONPikachu Outbreak！地点：日本横滨日期：2018年8月10日 — 8月16日地址：Minato Mirai area of Yokohama- E N D -谢谢你看到这里，希望你喜欢今天的推送。文 | 日和手帖图 | 日和手贴',
                     'Author': '什么值得吃', 'Time': 1534156590000, 'AddOn': 1534301212000})
    }]

url0 = 'http://101.71.28.12:12007/'
url1 = 'http://115.231.251.252:26016/'
url2 = 'http://60.190.238.168:38015/'
body = json.dumps(body_one)

# body = body_one
print(body)

r = requests.post(url0, data=body)
print(r.status_code)
print(r.text)

url = 'http://27.17.18.131:38072'
r = requests.post(url1, data=body)
print(r.status_code)
print(r.text)

print("=====")
r2 = requests.post(url2, data=body)
print(r2.status_code)
print(r2.text)
