# -*- coding: utf-8 -*-
import re
from collections import Counter

import jieba

class O(object):
    def __init__(self):
        self.name = 1


content_all_list = '感谢您关注教师帮微信！如果您尚未关注，请点击“教师帮”关注我们来源：周冲的影像声色（zhouchong2017）老师小磊哥说小磊哥的同事说，女人都很专一，只喜欢能给自己安全感的男人。而女人对安全感的定义，无非是陪伴还有金钱。可是，作为一名男教师，陪伴，给了学生。金钱，从踏上讲台那刻起，清贫或许就是他的符号吧。1今年春节，表哥进行了第八次相亲。表哥是一名农村教师。前面7个姑娘，全因为嫌表哥太穷，最后不欢而散。这第8个姑娘，是唯一不嫌弃表哥的。但因为两个小事，这段感情还是吹了。第一个事，两人去看电影。从电影开播到结束，两人谁也没看懂剧情。为什么呢？因为表哥不停地在接电话。“喂，你好，哦那个XX学生的家长吧，他打架的事情学校是这样处理的······”看了不到十分钟，电话又起。“孩子校服的费用不是我定的，是学校的意思，您要理解下····”这时，姑娘不开心了，说：“手机不能关掉吗？”表哥说：“我是班主任，周末手机关机不太好。”一场电影下来，个人手机成了电话热线，就没个消停。2第二个事，上课不能接电话。有一次，姑娘把脚扭伤了。因为需要有人扶她去医院，就打电话给表哥。第一个，被挂了。第二个，又被挂了。第三次打过去，他居然关机了。直到傍晚，表哥才出现在她面前。表哥满怀内疚地说：“对不起，我当时在上课，不能接电话。”那一瞬间，姑娘失望至极，含泪说道：“你身为一个教师，没钱，没时间，没自由，你拿什么给我幸福？”表哥的相亲趣事，后来成了我们当地的一个饭后谈资。并总结出一句话：当教师的，不配娶老婆。当然，此话在江湖上，早有传闻。比如，娶妻不娶护士，嫁郎不嫁老师。比如，相亲市场上的一线男老师，多是甩尾货。因为他们，不懂浪漫，也没时间搞浪漫；不配有爱情，也没条件哄女孩开心。有人说，这可是人类灵魂工程师，是太阳底下最光辉的职业呀。是的，曾经是。那又是什么，他们现在变得如此卑微了？31，穷有些人的穷，可能是暂时的。教师的穷，却像是一片望不到尽头的荒漠。我先拿出一组数据说话。这是去年年底，某相关机构做出的一个全国调查统计。﻿﻿北京，上海，准一线城市。普通教师工资在5000/月左右，加上各种奖金，也撑死不过6000/月。对体制内教师们而言，最高的天花板，也不过是高级教师。以为工资就很高吗？他们年薪，也不过10万左右。连一个快递小哥工资， 都还比不上。当然，这还是平均教师工资最高的几个城市。最低的，就更惨不忍睹。﻿﻿河南一老教师，教龄35年，月薪仅2800元/月。宁夏一乡村教师，到手仅2460元/月。湖南一优秀教师，月薪仅2340元/月。·····老师们常自嘲：自己是操着卖白粉的心，挣着卖白菜的钱。我怎么觉得，卖白菜都比这挣得多？如果你说，补课费呢？当家教呢？挣外快呢？教育部早已发过相关文件，严禁教师有偿补课。﻿﻿这是信息化的时代。学生随便一个投诉电话，一个采证视频，轻则降级处罚，重则丢了饭碗。没有多少老师，傻到去冒这个险。更恐怖的是，教师的穷，会伴随终生。工资涨的速度，跟不上货币贬值的速度。体制内教育行业的天花板，就那么点高。你会发现，就算拼尽全力做到了特级教师，或优秀班主任，自己依然还是个穷酸样。吃不饱，饿不死，买不起像样的轿车，付不起望而生畏的首付。只能这样，一直苟延残喘着。42，忙表哥说：“你知道当老师怕听到什么吗？”“说你们乱收费？”“不！最怕别人一听到教师，就酸溜溜地说：啊，你们好悠闲，一天就上两三节课，还有寒暑假，肯定很爽吧！”真实情况呢？教师的苦，是外人看不到的。教育部规定，工作时间为5天8小时制度。但实际情况，一般乡镇学校，6：45开始早读，老师必须到场，直到晚上5：15放学。你以为放学就没事了？一批事情等着你做。备课、改作业、开导学生、找家长谈话、应付领导检查·····如果还要上晚自习，那你算是彻底的“蜡炬成灰泪始干”。要从早上6：45，工作到晚上10:00。如果再逢上什么中考、高考，你的时间基本就全奉献给学生了。班主任的手机，永远是热线电话。平时教导学生，周末就沟通家长，总之，你基本天天围着这群学生转。知乎有个提问：嫁给一名老师是种什么体验？其中一个高赞回答：单身 too。没时间谈恋爱、没时间陪家人，没时间去活的像一个正常人。这就是教师们，真实的生活写照。53，窝囊“你看，老师也会打麻将哎。”“作为老师，怎么也那么爱钱？”“学生这点事都管不好，怎么当老师的？”·····这些话，是不是很熟悉？教师这个职业，在过于被神圣化之后，社会便对它进行了双标。发工资的时候，按下线标准；承担责任的时候，按上线标准。所以，当一有问题出现，矛头便指向了老师。比如四川一班主任，在高考结束后，被两名学生家长打进医院。比如安徽一女教师，因批评了学生，惨遭学生家长一顿暴打。社会对老师要求之苛刻，让无数从师者，人人感到自危。你要不管，领导说你没能力，家长说你不负责。你要管，面对一群熊孩子，打不得，骂不得，甚至连跟家长打电话时，你心都提到了嗓门眼。你做好了，这是你为人师表的本分。你做不好，这是你的无能。这其间的窝囊，怕是做过老师的人，才能真正体会。6做老师，最怕孩子会步自己的后尘。之前看过一个新闻，教师基本都不愿意让自己的孩子，也选择从事教师。﻿﻿37个教师子女，仅有一个女生，愿意填报师范院校志愿。看似震惊，其实也是情理之中。做了老师，大富大贵，你别想了。做了老师，起早贪黑、操心不断，已成常事。做了老师，潇洒和自由，便成了空中阁楼、镜花水月。曾在问答网看过一段话：“大多数女孩不愿意嫁给教师，因为从长远看，教师这个行业是个半封闭行业。”“整天与学生打交道，久而久之在人际交往上会有所欠缺，慢慢会与社会脱节。再加上如果不是领导阶层，对于一个家庭来说，生活档次也会降低。”老师穷，已是不争的事实。再加上社会的偏见，时间的不自由，工作环境的封闭，和看不见希望的未来，少有姑娘愿意嫁给他们，也就不足为奇了。毕竟，斯是陋室，惟吾德馨的年代，早过去了。有钱，才能捍卫爱情。有时间，才能经营好婚姻，可这些，老师们都没有。他们可能，只有一屋子优秀教师奖状，和一副因长期吸入粉尘，而患上慢性咽喉病的嗓子。显然，这是不公的。所以，有的老师去了培训机构，有的老师选择了“世界那么大，我想去看看”。但更多的人，还是留了下来。或为孩子，或为心中那仅存的一点信念。写在最后：《圣经》上说：为众人报薪者，不可使其冻毙于风雪；为自由开路者，不可使其困顿于荆棘。愿这个社会，能给一线教师们，一个更好的生存环境。愿看到此文的读者，能给他们，多一份理解和尊重。热文推荐：（点击蓝色字体阅读）◆紧急！又有一老师微信被盗，多名家长被骗转账！老师已赔近10万，微信群中的老师应该怎么避免此事发生！◆35岁女教师携女自杀身亡：那些从不生病的老师，其实早已遍体鳞伤◆2018高考毛坦厂中学放榜, 成绩再次刷爆网络! 泯灭人性还是为了尊严?◆招教遇冷：当年的“学渣”将成为你孩子的老师，轻师者闻之雀跃吗？◆临近退休教师不满“形式主义”辞职 ：世界虽然大，请别逼着老师去看看注：教师帮公众号长期接受作者投稿，单篇稿费100元-1000元不等，后台回复：“投稿”查看详情。作者：卓绝，一个有六块腹肌，和一腔才华的自由撰稿人。高级健身教练，“周冲的影像声色”签约作者。本文经授权转自微信公众号“周冲的影像声色”（zhouchong2017），这是一个文艺而理性的公众号，以文艺的笔调，以理性的思维，剖析人间事与人间情。我们的10万+和爆款文章教育点评类：寒门贵子｜惩罚学生｜工资不再跟职称挂钩｜教师点红包｜老师说事｜教师地位｜教师尊严｜老师去卖烧饼｜高考神话｜自我保护｜班主任就是包工头教师感悟：拿老师说事｜老师被举报｜教师扶贫｜老师紧箍｜你与成功的距离｜教师子女真相｜戒尺还给老师｜班主任忠告｜讨个教师做老婆｜老师“放弃”孩子｜我辞掉了｜教师帮公众号，隶属于三好网，是一个汇集数十万教师的优质交流学习社区。教师帮，帮老师，助力每一位教师成为真正的好老师。扫瞄二维码，进入教师帮咨询、交流请加小磊哥微信：sanhaolyg；投稿请发送至：1689029772@qq.com戳原文，做高薪教师！'
with open('positive.txt', 'r', encoding='utf-8') as f:
    positive = f.read()
with open('nagetive.txt', 'r', encoding='utf-8') as f:
    nagetive = f.read()

key_words_list = []
seg_list = jieba.cut(''.join(content_all_list), cut_all=False)
for i in seg_list:
    if len(i) >= 2 and re.match('[\u4e00-\u9fff]+', i):
        key_words_list.append(i)

# 返回前10个出现频率最高的词
key_words_counter = Counter(key_words_list).most_common()
key_word = dict()
key_word['list'] = []
for k in key_words_counter:
    key_word['list'].append(
        {
            "times": k[1],
            "keyword": k[0]
        }
    )
key_list = list(key_words_counter)
print(len(key_list))
count_positive = 0
count_nagetive = 0
for key in key_list:
    k, c = key
    if k in positive.split('\n'):
        count_positive += c
        # print(k)

    if k in nagetive.split('\n'):
        count_nagetive += c
        # print('k2', k)
print(count_positive)

print(count_nagetive)
