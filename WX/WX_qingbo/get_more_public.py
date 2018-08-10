import datetime

import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymongo
import urllib.parse
import os
import pymysql
from send_backpack import JsonEntity, Acount, Article
from pyquery import PyQuery as pq
# conn = pymongo.MongoClient('127.0.0.1', 27017)
# urun = conn.urun

current_dir = os.getcwd()
log_dir = os.path.join(current_dir, 'wx_log.txt')

MYSQL_HOST = '192.168.1.21'
MYSQL_PORT = 8001
MYSQL_USER = 'user'
MYSQL_PASSWORD = 'ABCd1234'
MYSQL_DATABASE = 'mysql'

config_mysql = {
    'host': MYSQL_HOST,
    'port': MYSQL_PORT,
    'user': MYSQL_USER,
    'db': MYSQL_DATABASE,
    'passwd': MYSQL_PASSWORD
}

db = pymysql.connect(**config_mysql)
cursor = db.cursor()


def log(*args, **kwargs):
    time_format = '%y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)
    with open(log_dir, 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


class PublicDetails(object):
    def __init__(self):
        self.driver = None
        self.name = ''
        self.read_num = ''
        self.praise = ''
        self.name_list = []

    @staticmethod
    def get_driver():
        # 使用headless无界面浏览器模式
        # options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # driver = webdriver.Chrome(chrome_options=options)

        driver = webdriver.Chrome()
        # driver = webdriver.PhantomJS()
        return driver

    @staticmethod
    def date_to_timestamp(before_time):
        # 格式化时间 '2017-03-16 18:22:06'
        ts = time.strptime(before_time, "%Y-%m-%d %H:%M:%S")
        return str(int(time.mktime(ts)))


    def get_public_name(self):
        url = 'http://183.131.241.60:38011/nextaccount?label=0'
        resp = requests.get(url)
        # print(resp.text)
        datas = json.loads(resp.text)
        name_list = []
        for d in datas:
            name = d.get('name')
            name_list.append(name)
        log('name_list', name_list)
        return name_list

    def login_website(self):
        if self.driver is None:
            self.driver = self.get_driver()
        url = "http://www.gsdata.cn"
        self.driver.get(url)
        time.sleep(2)
        register_login = self.driver.find_element_by_class_name('useinfo').find_elements_by_tag_name('a')
        login = register_login[1]
        login.click()
        time.sleep(3)
        input_button = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/a[2]/img')
        input_button.click()
        time.sleep(2)

        login_button = self.driver.find_element_by_xpath('//*[@id="login-form"]/div/div[1]/input')
        password_button = self.driver.find_element_by_xpath('//*[@id="login-form"]/div/div[2]/input')

        login_button.send_keys('18390553540')
        password_button.send_keys('qb123258456')
        button = self.driver.find_element_by_xpath('//*[@id="login-form"]/div/div[4]/button')
        time.sleep(1)
        button.click()
        time.sleep(2)

    def get_numb(self, name, count):
        # 50次重新定位到搜索主页
        if count % 500 == 0 and count != 0:
            print("重置主页")
            if self.driver is not None:
                log(self.driver.current_url)
                self.driver.quit()
            self.driver = self.get_driver()
            self.login_website()
            time.sleep(3)
        # 点击搜索
        search_input = self.driver.find_element_by_xpath('//*[@id="search_input"]')
        name = 'cube'
        search_input.clear()
        search_input.send_keys(name)
        search_button = self.driver.find_element_by_class_name('search_wx')
        search_button.click()
        time.sleep(2.5)


        # 发包列表

        backpack_list = [
    {
        "headers": {
            "topic": "datacenter",
            "key": None,
            "timestamp": int(time.time())
        },
        "body": "["
                "{\"headers\":{\"topic\":\"datacenter\",\"ip\":\"115.231.251.252:26016|60.190.238.168:38015\",\"key\":\"f855a40600f26febbe210d381385ce98\",\"timestamp\":1533716580848},\"body\":\"{\\\"ID\\\":\\\"f855a40600f26febbe210d381385ce98\\\",\\\"TaskID\\\":\\\"51825712\\\",\\\"TaskName\\\":\\\"微信_掌上平度\\\",\\\"AccountID\\\":\\\"51825712\\\",\\\"GroupName\\\":\\\"微信\\\",\\\"SiteID\\\":51825712,\\\"Language\\\":1,\\\"Channel\\\":20,\\\"Url\\\":\\\"http://mp.datacenter.qq.com/s?timestamp=1533716578&src=3&ver=1&signature=tgSlOV8*FQ08pfmNjh8ge4c8FQsssKhoopUphbmfTvAOSft-XdiSBbah5Vfg5L73VR4aTAD8cCBOXkTPSX2V6Eddtn101zSOTYJXL3HekXNs8BpOBnWKfrVaxTvrO12vw23rl-zroD7eqVZ3JSpNv5PqL3BHWtr7AN7eKfu-ILk=\\\",\\\"Title\\\":\\\"21岁通辽大学生在父亲的怀里停止了呼吸，原因值得所有家长警醒！\\\",\\\"Content\\\":\\\"\\\\n                    \\\\n\\\\n                    \\\\n\\\\n                    \\\\n                    \\\\n                    ◆来源：法制与新闻◆本文版权归原作者所有，如有侵权请联系我们18日上午，跪在医院的病床上，时而狂躁大喊将床单撕成碎条，时而安静下来紧紧盯着自己的父亲，眼神中是满满的恐惧和不舍。在父亲从通辽赶到包头市三医院50分钟后，刘显飞在父亲的陪伴下彻底停止了呼吸。年仅21岁的大二学生刘显飞的生前照大学生忽然口水不止今年21周岁的刘显飞是包头轻工职业技术学院室内装潢与设计专业的大二学生。15日晚上，班主任杨敏忽然收到了刘显飞发来的一条微信：“老师，我有点难受，明天想请假去医院看病。”杨敏很痛快地同意了他的要求并嘱咐他早点休息。16日下午，刘显飞在包医二附院挂了急诊，随后给杨敏打了电话。“他给我打电话说他难受得厉害，我挂了电话就联系我丈夫一起去二附院陪他做检查。”在各项检查未发现异常后，杨敏为刘显飞在医院附近租了一间宾馆住下，并让3名同学留下陪同，准备第二天继续检查。17日一早，陪同刘显飞的同学给杨敏打去电话，称刘显飞症状不仅没轻，反而开始不停呕吐并流口水。杨敏随后给刘显飞远在通辽的父母亲去了电话，商量后，决定带刘显飞换家医院试试，于是，几人打车赶往包头市中心医院。　　被咬伤没出血他没打狂犬疫苗得知刘显飞的情况后，大夫当时便问他近期有没有被小动物咬过。杨敏说，由于当时刘显飞十分难受，他想了很久这才想起在6月下旬，自己曾在路边被小动物咬过。6月下旬的一天，刘显飞在外出返校途中蹲在马路旁边系鞋带，一个小狗冲了过来，他在用手去驱赶小狗时，大拇指划到了小狗的牙齿，肉皮虽破但没有出血。因为家庭情况特别贫困，所以刘显飞没舍得去花好几百元打狂犬疫苗，也没告知父母让他们担心。在他看来，没出血应该就不严重。在中心医院传染科内，医生查看了刘显飞的病情，初步怀疑是狂犬病的症状。“主任当时表示让我们赶紧转三医院的传染科，别耽误。”杨敏说。青年遗憾离世17日晚，在医院病房内的刘显飞开始出现狂躁症状，他青筋暴露不停嘶吼，将病房的床单被罩撕得粉碎。刘显飞用手机上网查了狂犬病的相关信息，担心自己犯起病来会伤到他人，于是不停跪在床上双手作揖，让所有人都退出病房。“他已经知道自己的病治不好了，他一直在等他的父亲，他说自己只想再见父亲一面，给父亲磕个头就离开。”刘显飞的主治医生、市三医院传染科主任毛红说。18日上午10点，刘显飞的父亲终于赶到了儿子的病房，看到孩子第一眼时，这个皮肤黝黑看上去非常结实的男人哭出了声。他紧紧抱住儿子不停说着：“别怕，爸爸来了，病能治好。”他能明显感觉到小飞一直在克制着自己，不让自己狂躁，他能感觉到儿子想在生命的最后时刻安静地和他待会儿。10时50分，躺在父亲怀里的小飞开始昏迷，尽管医生尽力抢救，小飞最后还是离开了人世。在父亲、老师、同学、医生、护士们的陪伴下，永远的闭上了眼睛……现在正是高发季专家提醒：市民不要故意逗弄猫狗等动物，以免被抓伤或咬伤。人被病犬咬伤后发病率为15%-20%，被健康的狗狗咬伤则无碍，因此喜欢养宠物的市民一定要给猫狗接种疫苗。 从我国现有的狂犬病病例来看，大多数病例的潜伏期为半年以内，一般为半个月至三个月。在发病后会感到咬伤部位异常或刺痛，接着出现恐水、畏光、吞咽困难、狂躁等，随后发生瘫痪、昏迷，死亡。狂犬病一旦发病，其病程发展很快，多数人在3至5天死亡。病发前均可接种疫苗专家提醒：许多人对狂犬疫苗有严重认识误区，民间存在着“48小时有效”、“72小时有效”的说法。这种错误认识，曾直接导致了死亡案例。事实上，被狗咬伤或抓伤后，当然是越早接种狂犬疫苗越好，但并不存在时效性，只要在发病前，按要求全程接种，均可以起到有效免疫作用。不要私存，放到圈子里，让更多人知道吧！1.你可以将它传扬出去，传播一些积极正面的信息，让世间多一点爱。2.你也可以根本不去理会它，就像你从未看见一样。（绿岸荐读）公益广告总   编/綦   霏副总编/张泉水  杨江涛编   辑/山东省平度市新闻中心全媒体技术总监/宋嘉山联系电话/(0532)88321086\\\\n                \\\",\\\"Author\\\":\\\"掌上平度\\\",\\\"From\\\":null,\\\"Time\\\":1533711728000,\\\"Images\\\":9,\\\"ImageUrl\\\":\\\"https://mmbiz.qpic.cn/mmbiz/xP5v4lRAOibHdLIGXm8nU9xB7UIV2aib43Qw4B74bTPoygK9TWq58qYBdvydMfc2ErzAxDkfE0rpFl1GzMicDEpqw/640?wx_fmt=gif|https://mmbiz.qpic.cn/mmbiz_jpg/g3C2d3kcdJa3obJkiaxL9FrQjxSR6ibhNZsbyxjIIc93Hmc7vLj5iaE1zEvIV3FwsOaW5EcuBeFay8jPKtBDyHQHQ/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_png/g3C2d3kcdJa3obJkiaxL9FrQjxSR6ibhNZbUSVib3qlzzTz9u7ST1EiaRCqiasGDvwRCv04X7Y2AwHx5BXNKLeUXzWQ/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_jpg/g3C2d3kcdJa3obJkiaxL9FrQjxSR6ibhNZYdFNy2ibrArytVib99zw10Hfdib3buKq8Ijia9HicYxF3WRlfXyyvW1YJcw/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_png/g3C2d3kcdJa3obJkiaxL9FrQjxSR6ibhNZRFWvyiaO8QJ3wQCNNMtPlWqSCvImcbooJdDRTpjZKpqhEXWPjJAjmXQ/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_jpg/76CPRCM3dvXQboybY4X79fQZlz075HKQEXJu9jTsTAoMfcbvj4ghJnMiaCJKBRcnmRq2NpNERaVpwvnbBfhcHVw/640?wx_fmt=jpeg|http://mmsns.qpic.cn/mmsns/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakiazCJgcsXxj4oibzBEMlSibJA/0?wx_fmt=png|http://mmsns.qpic.cn/mmsns/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakujLlDWkMicRHmDenu2z36rQ/0?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakkiafMmGRWPCsIPeicHfibclVFrhJKiczLiaW30VWGZBVOM73URBWicgzNb4A/640?wx_fmt=jpeg\\\",\\\"Views\\\":0,\\\"Praises\\\":0,\\\"Place\\\":null,\\\"Person\\\":null,\\\"Keyword\\\":null,\\\"Hash\\\":\\\"\\\",\\\"ParagraphHash\\\":\\\"\\\",\\\"TopicID\\\":0,\\\"AddOn\\\":1533716580000,\\\"TitleSegment\\\":null,\\\"DefinedSite\\\":null,\\\"CustomerID\\\":\\\"\\\",\\\"Account\\\":\\\"zspd0532\\\",\\\"Pure\\\":null,\\\"Pureadj\\\":null,\\\"IsOriginal\\\":false,\\\"OriginalUrl\\\":\\\"\\\",\\\"IsHeadline\\\":true,\\\"Departments\\\":null,\\\"Companies\\\":null,\\\"Brands\\\":null,\\\"newsContent\\\":null,\\\"Tags\\\":null,\\\"IsGarbage\\\":0,\\\"Positive\\\":0,\\\"Negative\\\":0}\"},{\"headers\":{\"topic\":\"datacenter\",\"ip\":\"115.231.251.252:26016|60.190.238.168:38015\",\"key\":\"3a2ca786db29b54b25860a03f5136d41\",\"timestamp\":1533716582488},\"body\":\"{\\\"ID\\\":\\\"3a2ca786db29b54b25860a03f5136d41\\\",\\\"TaskID\\\":\\\"51825712\\\",\\\"TaskName\\\":\\\"微信_掌上平度\\\",\\\"AccountID\\\":\\\"51825712\\\",\\\"GroupName\\\":\\\"微信\\\",\\\"SiteID\\\":51825712,\\\"Language\\\":1,\\\"Channel\\\":20,\\\"Url\\\":\\\"http://mp.datacenter.qq.com/s?timestamp=1533716578&src=3&ver=1&signature=tgSlOV8*FQ08pfmNjh8ge4c8FQsssKhoopUphbmfTvAOSft-XdiSBbah5Vfg5L73VR4aTAD8cCBOXkTPSX2V6Eddtn101zSOTYJXL3HekXO1x3kRLV4wNToCBs59Yvo0KWzfR42vUv122eZ-9yVdT1TN7367xSOp14ezKu*yu-c=\\\",\\\"Title\\\":\\\"好消息：平度这些人的电费要退了！！！\\\",\\\"Content\\\":\\\"\\\\n                    \\\\n\\\\n                    \\\\n\\\\n                    \\\\n                    \\\\n                    ◆来源：山东潍坊综合整理◆本文版权归原作者所有，如有侵权请联系我们昨天已经立秋了 立秋意味着夏季结束秋季即将开始“一候凉风至，二候白露降，三候寒蝉鸣”我国地域辽阔各地气候有差别立秋之后大部分地区暑气难消平度的小伙伴们也要注意提防“秋老虎”这周咱们平度的天气用四个字来形容就是“又热又闷” 多云 - 多云 - 多云 本周最高气温竟然还是35℃！哦，不！没有太阳！“明热易躲，暗热难防啊！\\\\\\\"小伙伴们，别担心！热就热呗！闷就闷呗！反正我有空调~而且！重点是！平度要退电费了！！！我的平度兄Dei！我没有在哄你玩儿~喏！看下面！山东省物价局关于降低工商业电价有关事项的通知▼各市物价局，国网山东省电力公司：根据国家发展改革委《关于电力行业增值税税率调整相应降低一般工商业电价的通知》（发改价格〔2018〕732号）规定，为进一步降低工商业电价，经省政府同意，现将我省电价调整有关事项通知如下：一、降低工商业电价执行政府定价用户，单一制电价每千瓦时降低0.019元（含税，下同），两部制电价降低0.0034元；参加电力市场直接交易用户，单一制输配电价降低0.0218元，两部制输配电价降低0.0062元。调整后标准详见附件。二、扩大系统备用费减免范围将分布式天然气发电、沼气发电、风力发电等清洁能源纳入系统备用费减免范围。具体申报流程按照《山东省物价局关于明确临时接电费和自备电厂有关价格政策的通知》（鲁价格一发〔2017〕127号）有关规定执行。三、有关要求上述电价政策自2018年5月1日起执行。已经收取5月份电费的用户，由国网山东省电力公司按照5月份实际抄见天数折算差额电费进行退费。各级价格主管部门要加强监管，确保电价政策执行到位。附件：山东省物价局2018年6月22日惊不惊喜！意不意外！你们家退电费了没？公益广告总   编/綦   霏副总编/张泉水  杨江涛编   辑/山东省平度市新闻中心全媒体技术总监/宋嘉山联系电话/(0532)88321086\\\\n                \\\",\\\"Author\\\":\\\"掌上平度\\\",\\\"From\\\":null,\\\"Time\\\":1533711728000,\\\"Images\\\":12,\\\"ImageUrl\\\":\\\"https://mmbiz.qpic.cn/mmbiz/xP5v4lRAOibHdLIGXm8nU9xB7UIV2aib43Qw4B74bTPoygK9TWq58qYBdvydMfc2ErzAxDkfE0rpFl1GzMicDEpqw/640?wx_fmt=gif|https://mmbiz.qpic.cn/mmbiz_jpg/cTsjLMjYjXkMQmFXNj5icoVGdoxicHf3AYOgFRe73KQnjWNFMNQ4NPpGMic14Gj8gmXWBlVg2q9uJSjW1BaNlibLxQ/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_png/xP5v4lRAOibHqx6r1HdXtrSjLYbycI7p0ibOAhuVmSS5BguyeDUEXxUVXzyibDsibHF4sXNjLyBvJmUrkokI9hMArA/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_gif/cTsjLMjYjXkMQmFXNj5icoVGdoxicHf3AYEebX4eAWwL9RWm2Tqibl10dVdQryJ3UayWwlIm9YepDH4wUo5vSqMwQ/640?wx_fmt=gif|https://mmbiz.qpic.cn/mmbiz_gif/cTsjLMjYjXkMQmFXNj5icoVGdoxicHf3AYl8tjicx0nBdOfmSAia9DjO9pIRbZ9YOiaNeolcjNWWBEfpqyjiaSv8iaNBg/640?wx_fmt=gif|https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWgEF8Um574KqtEYjlfYazBQRKDIqGtBX7qpHLxOW1Hclib9CW20S6ZQped9YPr93cnBZCM0F2cjKQQ/640?wx_fmt=gif|https://mmbiz.qpic.cn/mmbiz_png/rPX8S940libwAUZewHIBUXKjry4ub4nxPJfNGXGwlYquj5QzN089ezcLyvpxgaBuG1ficS5oFwmzcr2RWXxvlqQg/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_png/rPX8S940libwAUZewHIBUXKjry4ub4nxPGNrlg5nZoCCJqXI8v0VulCjSCOSW0ZmWLYcklyxNSh4Hpz1dAsHhBw/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_jpg/76CPRCM3dvXQboybY4X79fQZlz075HKQEXJu9jTsTAoMfcbvj4ghJnMiaCJKBRcnmRq2NpNERaVpwvnbBfhcHVw/640?wx_fmt=jpeg|http://mmsns.qpic.cn/mmsns/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakiazCJgcsXxj4oibzBEMlSibJA/0?wx_fmt=png|http://mmsns.qpic.cn/mmsns/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakujLlDWkMicRHmDenu2z36rQ/0?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakkiafMmGRWPCsIPeicHfibclVFrhJKiczLiaW30VWGZBVOM73URBWicgzNb4A/640?wx_fmt=jpeg\\\",\\\"Views\\\":0,\\\"Praises\\\":0,\\\"Place\\\":null,\\\"Person\\\":null,\\\"Keyword\\\":null,\\\"Hash\\\":\\\"\\\",\\\"ParagraphHash\\\":\\\"\\\",\\\"TopicID\\\":0,\\\"AddOn\\\":1533716582000,\\\"TitleSegment\\\":null,\\\"DefinedSite\\\":null,\\\"CustomerID\\\":\\\"\\\",\\\"Account\\\":\\\"zspd0532\\\",\\\"Pure\\\":null,\\\"Pureadj\\\":null,\\\"IsOriginal\\\":false,\\\"OriginalUrl\\\":\\\"\\\",\\\"IsHeadline\\\":false,\\\"Departments\\\":null,\\\"Companies\\\":null,\\\"Brands\\\":null,\\\"newsContent\\\":null,\\\"Tags\\\":null,\\\"IsGarbage\\\":0,\\\"Positive\\\":0,\\\"Negative\\\":0}\"},{\"headers\":{\"topic\":\"datacenter\",\"ip\":\"115.231.251.252:26016|60.190.238.168:38015\",\"key\":\"3ced815a8f65c59183be3b0ce71607c8\",\"timestamp\":1533716584172},\"body\":\"{\\\"ID\\\":\\\"3ced815a8f65c59183be3b0ce71607c8\\\",\\\"TaskID\\\":\\\"51825712\\\",\\\"TaskName\\\":\\\"微信_掌上平度\\\",\\\"AccountID\\\":\\\"51825712\\\",\\\"GroupName\\\":\\\"微信\\\",\\\"SiteID\\\":51825712,\\\"Language\\\":1,\\\"Channel\\\":20,\\\"Url\\\":\\\"http://mp.datacenter.qq.com/s?timestamp=1533716578&src=3&ver=1&signature=tgSlOV8*FQ08pfmNjh8ge4c8FQsssKhoopUphbmfTvAOSft-XdiSBbah5Vfg5L73VR4aTAD8cCBOXkTPSX2V6Eddtn101zSOTYJXL3HekXOnnEGNWCK*lQJX0oGDtVh84l39EzWbfvt0ei-cK7ABtC0Y1mIrVpmL4tpiGE*NSzo=\\\",\\\"Title\\\":\\\"【特别关注】重磅：党报发文，房产税很快就来！平度这些人要颤抖了！\\\",\\\"Content\\\":\\\"\\\\n                    \\\\n\\\\n                    \\\\n\\\\n                    \\\\n                    \\\\n                    ◆来源：新京报◆本文版权归原作者所有，如有侵权请联系我们“据媒体报道，房产税的草案早已成形，决策部门这次决心很大，草案的征收幅度会超出很多人的预料。”8月6日，中共北京市委主管下的“新京报”发文称，房地产税出台的时机已基本成熟。新京报认为：一旦房价趋于全面平稳，就可以适时推出房地产税政策。在这样的情况下，相关的限购限贷限售等政策，也可以依据房地产税政策的执行情况，逐步退出。我们知道，世界上没有一直上涨永远不会下跌的资产；我们知道，一个以房地产为支柱的经济发展模式，是非常没有安全感的；我们知道，人均GDP只有美国八分之一，房价却能比肩跟纽约东京伦敦，这是有点逻辑不对的；我们知道，当房价不断上涨，居民收入却跟不上房价上涨速度的时候，接盘者会越来越少；我们知道，一个房屋空置率接近14%，比日本这种高度老龄化、少子化、城市化的国家还要高，这是非常不正常的；这些道理和经济逻辑我们都知道，但是房价为何还在上涨？原来，我们低估了人性的贪婪和险恶！当人拜房子为一种宗教的时候，当人陷入投资的癫狂状态时，当人成为乌合之众时，很多逻辑往往会被暂时颠覆，各种后果都会放置一边，为了追求心目找那个那一虚幻的刺激，会像飞蛾扑火一样，置生死于度外。但是万有引力的规律终归要起作用，飘得再高，也有回到地球的那一刻，只是起作用的时间会延后而已。那么中国城市房价真的会持续涨下去吗？很快，不少炒房的人会为当初的“炒高房价”付出代价。因为，房产税很快就要来了！据媒体报道，房产税的草案早已成形，决策部门这次决心很大，草案的征收幅度会超出很多人的预料。因为是按照房屋的市场评估价征收，所以，房价上涨的越多，有些人付出的房产税也会很多。当然，这个只是草案，会有一个征求意见和讨价还价的过程，草案本身是尺度比较大的，在讨价还价过程中，或许会有一些收缩，但大体方向不会改变——就是那些拥有多套房子，炒高房价的人，将有掩泪而泣的一天！其实，不动产登记全国联网完成后，在技术上房产税随时可以推出，但因为太多的阻力和不确定性，不断延后，包括像任志强这种所谓的开发商代言人，早获得风声，所以提前站出来反对。但这一次，恐怕反对也无效了。目前在河北等地，地方税务部门已经开始要求拥有房产的人填写家庭住房实有套数诚信保证书了，这个承诺是有法律和行政责任的。其实，房地产税落地，目前已有几重非常明显的信号。原则：立法先行、充分授权、分步推进今年3月份召开的全国两会上，财政部有关负责人在答记者问时表示：会按照中国国情合理设立房地产税制度。全国人大、财政部和相关部门正起草完善房地产税法律草案，总体思路是立法先行、充分授权、分步推进。4月27日，全国人大常委会公布2018年立法工作计划，房地产税法被列为预备审议项目，视情在2018年或者以后年度安排审议。立法先行、充分授权、分步推进的征收原则，12个字可谓高度概括：立法先行，指的是“税收法定”，房地产税落地，要经过人大立法；充分授权，指考虑到区情的不同，赋予地方以自主权；分步推进，指不同区域区情不同，房地产市场的健康程度也不同，地方对于税收的承受能力也有差别，房地产税只能分地区逐步推进。一句话：房地产税会充分考虑中国国情。地区发展水平不同，楼市区域分化，家庭购房负担突出，加上房地产相关税收繁多，这就意味着房地产税不会一刀切，肯定会照顾刚需，照顾经济相对弱势的城市，同时还要整合相关税收。国地税合并，为征收房地产税扫清障碍房地产税想要全面推行，必须满足一系列的技术条件。如今，这些技术障碍都已不复存在。3月份，今年通过的根本大法，明确赋予所有“设区的市”以地方立法权。这为房地产税分城市分区域征收提供了可能。毕竟，地方发展不同，楼市发展程度不同，居民承受程度不同，房地产税只可能“因城施策”。6月15日，全国省级国税地税合并挂牌完成，这标志着国地税合并迈出关键实质性步伐。国地税合并的最大意义，还不是减少交易成本和信息壁垒、降低人员冗余，而是统一税收监管，为个税、房地产税的征收铺路。地方立法权、国地税合并，这意味着征收房地产税在技术上也不再存在什么障碍。信号明显，房地产税真的要来了进入2018年以来，关于房地产税相关政策出台的声音越来越大。/ 全国联网登记不动产 /在今年端午节前后，出了一条信息：全国统一的不动产登记信息管理基础平台，目前已实现全国联网。不动产登记的全国联网，让开征房地产税的条件更加成熟！/ 国务院大督查 /在7月发布的《国务院关于开展2018年国务院大督查的通知》中指出：今年将继续选取包括“房产交易登记”、“获得信贷”等7项指标，对31个省(自治区、直辖市)进行调查评价。有业内人士指出：“针对房产交易登记的督查并非首次，但将其列入国务院大督查，则进一步表明了政府对于房地产市场的重视程度。”事实上，从去年以来，关于房地产税的表态就日益密集，透露的细节越来越多，涉及的层级越来越高，同时也不乏具体配套政策的落地。房地产税来了，网友怎么说？房子对中国人来说是刚需，所以任何的房产政策的出台和动向，所有人都十分地关心！正如最近这条#房地产税有望加快推进#消息一出，迅速爬上了微博热搜。效率够快↓↓↓开征房地产税的呼声一直很高，很多人以为会拖个几年，但是在你看不见的地方，政府正在稳步地推进，房地产税离我们真的不是很远了！房地产税怎么征？↓↓↓很多人最关心的问题就是房地产税怎么征收？如何保证公平？辛辛苦苦地买一套房，还要交税？从这位网友的评论中我们知道，并不是所有人都要交税的！个人住宅超过两套、三套住房可能才会被征税，在此基础上：第一，多占资源，多交税。我住100平，你住200平，你多交税。第二，占好资源多交税。你100平，我也100平。你市中心+学区房，我在大北边挨着工厂，你多交税。第三，生活用房、保障用房不用交税。希望尽快出台↓↓↓开征房地产税，直接影响那些恶意炒房团，手里有多套房的人明显要多征一些税，房地产税可能是他们的灭顶之灾！如果房地产税来了，谁最害怕？①在中心城市囤积了大量住宅的人伤害指数★★★从目前民意来看，在中心城市实施“累进制、惩罚性”的房产税，是很有可能的。对于拥有100套住宅的人来说，即便第一套免征、从第五套开始累进税率，他的压力也会非常大。到时候会出现集中抛盘，对中心城市短期房价构成影响。这可能意味着，囤积大量房子的人财富将显著缩水。②盲目购买了旅游物业、养老地产的人伤害指数★★★★如果不是顶级旅游区，不是配套好、位置佳的房子，旅游地产只能等着免征房地产税。如果不能免征，则其持有成本大增，加上利用率不高，这类房子将成为鸡肋。③盲目购买了三四线城市郊区、新区住宅的人伤害指数★★★★绝大多数三四五线城市人口增长乏力，各地围绕着高铁站建设的“高铁新城”很多都非常荒凉。如果盲目在这些地区购买了住宅，未来开征房地产税后也会非常惨。④加杠杆、超承受能力买多套房的白领伤害指数★★★★如果房地产税的开征，会让房价进入一个平稳期，房子很难套现。这些人“死扛现金流压力”的期限就会加长，生活会变得比较痛苦。 ⑤在三四线城市囤积了大量住宅的人伤害指数★★★★★★相对而言，这种人更惨。即便在三四线城市不实施累进制、惩罚性的房地产税，他们持有房产的成本将大增。但由于多数中西部三四线城市人口增长乏力，很多家庭都拥有多套房，所以很难通过出租转嫁房地产税，而卖房子很有可能出现无人买的情况。⑥手中有多套房、负债率非常高的炒房者伤害指数★★★★★★房地产税加快出台这个消息，就足以对这类人产生巨大的压力。因为消息公布后，会加剧市场的僵持，目前仍然拿了很多房子、承担巨大债务的炒房者，将会非常困难。他们只能选择斩仓，否则房子可能断供被银行申请查封、拍卖，到那时套现价格会更低。开征房产税是大势所趋也势在必行这一次，房产税离我们更近了…公益广告总   编/綦   霏副总编/张泉水  杨江涛编   辑/山东省平度市新闻中心全媒体技术总监/宋嘉山联系电话/(0532)88321086\\\\n                \\\",\\\"Author\\\":\\\"掌上平度\\\",\\\"From\\\":null,\\\"Time\\\":1533711728000,\\\"Images\\\":13,\\\"ImageUrl\\\":\\\"https://mmbiz.qpic.cn/mmbiz/xP5v4lRAOibHdLIGXm8nU9xB7UIV2aib43Qw4B74bTPoygK9TWq58qYBdvydMfc2ErzAxDkfE0rpFl1GzMicDEpqw/640?wx_fmt=gif|https://mmbiz.qpic.cn/mmbiz_jpg/xXgGFg9YqAw54qkany8SPKIZzwdtwqHnVia4JthgjwQF9ibxmHZxHS9cjQlXRT3Crwp1ZDjaeAicH63ODnRcXSs4A/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/pFgEYY3zZKlXI5zguLBrr2ma4Oum0gRPITmJ0mAc0nEQgB1Ltdt4O1EaaiaiczJyly38x9BlBuIrNibIeL7iaIaWyw/640?|https://mmbiz.qpic.cn/mmbiz_jpg/pFgEYY3zZKmgRY0e6M87lFibdug7lbd4diaqHkqQBbnDIZKTjVTmLAmpWLnOCMf3BLW2pmREyr9tNFPFCFVU8cIg/640?|https://mmbiz.qpic.cn/mmbiz_png/Wuerr0OnLdGOqWGQibgtMg5GKPYoB4wKyZffO4BlK2icZtBGUTKZ5VdotEkEPvQxZsYqp2eoc0tQ34jf7bezlagQ/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_png/1Xd8JoEFarFEWicHwbhloqrM1ZmHO7SrcwLaEzBeCmsfYkicGiay9nqUukEghicQGtJXQtiaEyfeMiaJgR51RktFwvxw/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_jpg/rZ2Q1k4D3aST3qWSQrOP9DmtcoDzHDRLeop7tdjCKnhnNicNZ0w11Db1KuzHVcwclcp2dsZ3wdJJ2pNuPkibxKaA/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/1Xd8JoEFarFEWicHwbhloqrM1ZmHO7SrcPBnoXYApQChnBw2jgscg1OPHMYzV1o3IOzkhduJv5oya95ruVibIMcw/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/1Xd8JoEFarFEWicHwbhloqrM1ZmHO7SrcH9k4rlwSlicibUs6iahbfMib8DrP1tTibC9GHsRTn8Rib39G78Hqc9CoheUg/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/76CPRCM3dvXQboybY4X79fQZlz075HKQEXJu9jTsTAoMfcbvj4ghJnMiaCJKBRcnmRq2NpNERaVpwvnbBfhcHVw/640?wx_fmt=jpeg|http://mmsns.qpic.cn/mmsns/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakiazCJgcsXxj4oibzBEMlSibJA/0?wx_fmt=png|http://mmsns.qpic.cn/mmsns/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakujLlDWkMicRHmDenu2z36rQ/0?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakkiafMmGRWPCsIPeicHfibclVFrhJKiczLiaW30VWGZBVOM73URBWicgzNb4A/640?wx_fmt=jpeg\\\",\\\"Views\\\":0,\\\"Praises\\\":0,\\\"Place\\\":null,\\\"Person\\\":null,\\\"Keyword\\\":null,\\\"Hash\\\":\\\"\\\",\\\"ParagraphHash\\\":\\\"\\\",\\\"TopicID\\\":0,\\\"AddOn\\\":1533716583000,\\\"TitleSegment\\\":null,\\\"DefinedSite\\\":null,\\\"CustomerID\\\":\\\"\\\",\\\"Account\\\":\\\"zspd0532\\\",\\\"Pure\\\":null,\\\"Pureadj\\\":null,\\\"IsOriginal\\\":false,\\\"OriginalUrl\\\":\\\"\\\",\\\"IsHeadline\\\":false,\\\"Departments\\\":null,\\\"Companies\\\":null,\\\"Brands\\\":null,\\\"newsContent\\\":null,\\\"Tags\\\":null,\\\"IsGarbage\\\":0,\\\"Positive\\\":0,\\\"Negative\\\":0}\"},{\"headers\":{\"topic\":\"datacenter\",\"ip\":\"115.231.251.252:26016|60.190.238.168:38015\",\"key\":\"2c4cb0b3adb381f1db8cab230f49a104\",\"timestamp\":1533716585820},\"body\":\"{\\\"ID\\\":\\\"2c4cb0b3adb381f1db8cab230f49a104\\\",\\\"TaskID\\\":\\\"51825712\\\",\\\"TaskName\\\":\\\"微信_掌上平度\\\",\\\"AccountID\\\":\\\"51825712\\\",\\\"GroupName\\\":\\\"微信\\\",\\\"SiteID\\\":51825712,\\\"Language\\\":1,\\\"Channel\\\":20,\\\"Url\\\":\\\"http://mp.datacenter.qq.com/s?timestamp=1533716578&src=3&ver=1&signature=tgSlOV8*FQ08pfmNjh8ge4c8FQsssKhoopUphbmfTvAOSft-XdiSBbah5Vfg5L73VR4aTAD8cCBOXkTPSX2V6Eddtn101zSOTYJXL3HekXPL18WiT4xzlrGB2YL*Kfy**RqRcppIFWS4HxnQvEWAbHQ0Q*Z8jNJwtBDSVomWu8Q=\\\",\\\"Title\\\":\\\"【今日平度丨平度新闻】2018年8月8日星期三\\\",\\\"Content\\\":\\\"\\\\n                    \\\\n\\\\n                    \\\\n\\\\n                    \\\\n                    \\\\n                    第1版：要闻第2版：时政·经济第3版：法制·社会第4版：副刊第5版： 党建·三农第6版： 综合第7版：文苑第8版：国内国际热点要闻▶6日，国务院调查组公布吉林长春长生违法违规生产狂犬病疫苗案件调查进展，长春长生从2014年4月起就存在严重违规行为。▶近日，我国天文学家依托郭守敬望远镜发现一颗目前人类已知锂元素丰度最高的恒星，锂元素含量约是同类天体的3000倍。▶当地时间6日，美国正式宣布重启对伊朗的制裁。伊朗总统鲁哈尼称，美国将会为实施制裁感到后悔。▶欧盟委员会6日宣布，欧盟最新反制裁条例将于7日生效，以保护在伊朗合法经营的欧盟居民和公司的利益。社会▶北京最大规模组织考试作弊案7日宣判，在全国研究生考试中组织30余名考生作弊的章无涯等6人，被处有期徒刑4年至1年8个月不等。▶网曝贵州纳雍一卫生室设“最低消费”，打针输液60元起。当地市场监督管理局7日回应，情况属实，将进一步调查处理。▶近日，四川仁寿的黄某某在微信群内发布对两名因公牺牲警察的侮辱言论，涉及广泛，影响恶劣，被刑事拘留。▶2022年杭州亚运会会徽“潮涌”6日发布，由扇面、钱江潮头、赛道、互联网符号等元素组成。▶6日晚，贵州盘州市梓木戛煤矿发生一起煤与瓦斯突出事故，已致4人死亡，9人失联。▶上海公布落户新政，清华北大本科毕业生符合基本申报条件可直接落户。▶安徽13名渔民自愿退出捕鱼业，加入安庆江豚协助巡护队，巡护队一年航行超4万公里，劝退非法捕捞近百起，清除垃圾65吨。▶湖北孝感4岁男孩从防盗网坠落，悬在20米高空。辅警李开红徒手攀上防盗网，托举孩子5分多钟，最终与众人合力救下孩子。▶3日，江苏铜山一男子跳河轻生，65岁老伯张开良跳河救人，在水中抱住落水男子半小时等待救援，在其他市民的配合下将男子救起。8月6日微博热点TOP 1网友评论我心向阳光面朝大海：多给工资吧，不容易啊！聆听朝阳的美好pan：辛苦了TOP 2网友评论昕昕Jocelyn：作为一个父亲不说自己没本事没能力撑起这个家，反而说儿子太急，相信大家都知道这个急背后的原因，这世过的太悲催了，祝福你下世心愿得以实现🙏乐清女郎：这个父亲绝对不是省油的灯啊！TOP 3网友评论走起路来带风：不是开除就能解决问题的书予空欢：夏令营CEO还自称也是受害者，就应该曝光！！让他倒闭！！追究法律责任！TOP 4网友评论晴欢少女：致敬，你们辛苦了老富贵_：他从火光中走来来源：广州日报 广州新闻电台 大洋网  新华社  央视新闻  人民日报  新浪微博 各大媒体电子数字报 去成为你想成为的人，什么时候都可以开始；去做你想做的事，任何方向都值得努力。吝惜汗水和能量，哪一条路都是弯路；朝着目标努力前进，整个世界都会为你让路。未来和梦想，不是想出来的，是拼出来的。公益宣传片《打击非法集资宣传片》总   编/綦   霏副总编/张泉水  杨江涛编   辑/山东省平度市新闻中心全媒体技术总监/宋嘉山联系电话/(0532)88321086\\\\n                \\\",\\\"Author\\\":\\\"掌上平度\\\",\\\"From\\\":null,\\\"Time\\\":1533711728000,\\\"Images\\\":24,\\\"ImageUrl\\\":\\\"https://mmbiz.qpic.cn/mmbiz/xP5v4lRAOibHdLIGXm8nU9xB7UIV2aib43Qw4B74bTPoygK9TWq58qYBdvydMfc2ErzAxDkfE0rpFl1GzMicDEpqw/640?wx_fmt=gif|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHqx6r1HdXtrSjLYbycI7p0zmKzSciaMMDSZsrIc0FjQldZBgtatl0IGgHpS2picUFlbnWjnWUnjgvw/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHqx6r1HdXtrSjLYbycI7p0ZC8GKTGjXV0Jk1KIUj0fiaXmN6icbX8icyHaTEtOXB2Q8Xk4auRRZ3tPg/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHqx6r1HdXtrSjLYbycI7p0FE22UohfT7W2Srnpibgk44wC5KToWhTRpWnxzCWy2oECVOaVjraVSmA/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHqx6r1HdXtrSjLYbycI7p0mwhsF3oWAlTFZoVqDw5274WicTUKfqlONkibbxsRvg2Os6CEI7uf9E2Q/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHqx6r1HdXtrSjLYbycI7p0RKiaPibf7DCHyzPcKSJKyYTqkibqPq6AbIJTiaRSViaxWkB2EepLk6tvHQQ/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHqx6r1HdXtrSjLYbycI7p0YWtibpJoQCw6pMf6BDH50hrlw7TO9ZuEwmuIAc4X7dL87HOwPeafexA/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHqx6r1HdXtrSjLYbycI7p0goUr6as6Wu3AKiaOiad9VsZQcMQ7fBfnMnycX1W8uRm775Hd00YcjnSQ/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHqx6r1HdXtrSjLYbycI7p0Nyn09Apia5uq8H8xxA9pI0X4tQFibZJEA51BNictTrOoickYqlEqThbu4g/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHqx6r1HdXtrSjLYbycI7p0JGaIDGDibst6v4iadntudYFuOnQ5lN4f74DAuV6DltIxB1t27NemicyHg/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xrFYciaHL08AYv7ETTWxOENIicklSzFJbNicBliaVO1tf5MHsvS7DCKvHliaibUVvZZP54TmJ39bQiaPOJWNQZke0jxMw/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xrFYciaHL08AYv7ETTWxOENIicklSzFJbNVrNXjIvHoQhBVWjic5BJEVevWkD66iaGj2GDbZrf2CfLDRPicDMe63knw/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xrFYciaHL08AYv7ETTWxOENIicklSzFJbNwDP94MsEcVp0BWUJIpbFiaiafzekGk9Yj8tgLucyvibHibaiaOBFggm036A/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xrFYciaHL08AYv7ETTWxOENIicklSzFJbNbyZpwmQjkJA4lFXYYZicR3DTvFQP0kVJoClJibiaxJGrf1X3OC5lePNKQ/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xrFYciaHL08AYv7ETTWxOENIicklSzFJbNOL0YatWUexho12NCjLD0k2MZXXJaLMhD3vkTLaFtm9DbA6gWMGmR7w/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xrFYciaHL08AYv7ETTWxOENIicklSzFJbNydLYMWHn2ichhWRbujfnS0icEvGGyic8IEmxCuxn1LSj2JGHxeQtzf1iaw/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/xrFYciaHL08AYv7ETTWxOENIicklSzFJbNJgLppkdlfOBric0rxhoIXsibG1TRZPVOEO8evPa1UibuPQQslf61icXPSg/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_png/RT9XD5E0r2Lx3hIS8BT2kFpHTqpibqqgxY9O7w9gfT8OubEs0Wzk5x8WdtZNR7XorzcDSNHlL96pErWL9iaQMA9w/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_png/RT9XD5E0r2Lx3hIS8BT2kFpHTqpibqqgxyA1ZgtXf9ZxvpcHU3HdGWXwzWoXrX3wAicZ5HM38x6r1iaibAicuz2y9bw/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_png/RT9XD5E0r2Lx3hIS8BT2kFpHTqpibqqgxC8mLFw1ibLAYp27tyy9p6GNricUg4d1CrSpPHCmib256JrhUSkWJmJnOg/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_png/RT9XD5E0r2Lx3hIS8BT2kFpHTqpibqqgxicMZ7mZTAOCdibiapJBDw5Tzw3DxkOPp4drNHnI6NPicSZlGQK0nuF5KWg/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_png/RT9XD5E0r2Lx3hIS8BT2kFpHTqpibqqgx7LjwM53bctiaGQW1V58xR1rfItLPibQtD9JgpPdAFibbZ6SibuPV0atMHg/640?wx_fmt=png|http://mmsns.qpic.cn/mmsns/xP5v4lRAOibG0NSuFlVuqAUS6ic9bjlibFEcsyibSUTJBl9ysPe5PQ6WcA/0?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHnmykTJxrOGFNlZPBKOKRRLb9oeVOslOOYySDN5KwV5KkeTcX7UVcKUAia7RichxJkGVk19r5hUibBA/640?wx_fmt=jpeg\\\",\\\"Views\\\":0,\\\"Praises\\\":0,\\\"Place\\\":null,\\\"Person\\\":null,\\\"Keyword\\\":null,\\\"Hash\\\":\\\"\\\",\\\"ParagraphHash\\\":\\\"\\\",\\\"TopicID\\\":0,\\\"AddOn\\\":1533716585000,\\\"TitleSegment\\\":null,\\\"DefinedSite\\\":null,\\\"CustomerID\\\":\\\"\\\",\\\"Account\\\":\\\"zspd0532\\\",\\\"Pure\\\":null,\\\"Pureadj\\\":null,\\\"IsOriginal\\\":false,\\\"OriginalUrl\\\":\\\"\\\",\\\"IsHeadline\\\":false,\\\"Departments\\\":null,\\\"Companies\\\":null,\\\"Brands\\\":null,\\\"newsContent\\\":null,\\\"Tags\\\":null,\\\"IsGarbage\\\":0,\\\"Positive\\\":0,\\\"Negative\\\":0}\"},{\"headers\":{\"topic\":\"datacenter\",\"ip\":\"115.231.251.252:26016|60.190.238.168:38015\",\"key\":\"2811c56be29972cc04e26dfb50a67e86\",\"timestamp\":1533716587456},\"body\":\"{\\\"ID\\\":\\\"2811c56be29972cc04e26dfb50a67e86\\\",\\\"TaskID\\\":\\\"51825712\\\",\\\"TaskName\\\":\\\"微信_掌上平度\\\",\\\"AccountID\\\":\\\"51825712\\\",\\\"GroupName\\\":\\\"微信\\\",\\\"SiteID\\\":51825712,\\\"Language\\\":1,\\\"Channel\\\":20,\\\"Url\\\":\\\"http://mp.datacenter.qq.com/s?timestamp=1533716578&src=3&ver=1&signature=tgSlOV8*FQ08pfmNjh8ge4c8FQsssKhoopUphbmfTvAOSft-XdiSBbah5Vfg5L73VR4aTAD8cCBOXkTPSX2V6Eddtn101zSOTYJXL3HekXMTuwl7MJtbSibBBTWfCsQZhujvnyzSKWaVPNNF19zzIRAwLq-Uso6ATPyk98kNh8E=\\\",\\\"Title\\\":\\\"【企业之光】全平度侧耳听！“美好平度从新聆听”钜献全城\\\",\\\"Content\\\":\\\"\\\\n                    \\\\n\\\\n                    \\\\n\\\\n                    \\\\n                    \\\\n                    1也许你走过很多地方，路过很多世间美景，听过无数动人的乐章，在匆忙前进的路上，你是如何记录你和平度这座城的故事？是那一个朝夕相伴的人？还是某一处你牵挂的地方？继“美好平度从新看见”首部城市之作唤醒平度人内心美好之后，第二季视频再次从一个全新的视角，给了我们一个惊喜的答案——用声音记录平度，在那些熟悉声音的讲述下，我们大平度竟然如此生动！2跟随视频主人公一起，用声音打开平度故事，你一定会感到很亲切，老邻居亲切的问候、孩子干净的欢笑声、公园里热闹的聚会声……循着那些回响在平凡岁月里的声音，寻见的其实就是你我踏实生活的足迹。我们生活的平度，少了些浮华喧嚣，却多了些美好从容；我们生活的平度，少了些疏离冷漠，却多了些温暖真情；我们生活的平度，少了些步履匆忙，却多了些闲适平和。3这就是缓缓浸润在你我身边的平度，在这里你我思量着油盐酱醋茶的平淡日常，在这里你我扎下安身立命的根，在这里你我肩负起孩子成长的每一个明天，在这里你我陪伴老爸老妈安享天伦……4当声音化成讲述者，平度的城市故事就显得格外动人和美好。感恩这座美好的城市，如此美好的平度，值得我们一起从新发现！据悉，后续将有更多精彩的平度故事跟我们分享，敬请期待！未完待续悦隽大都会艺术中心悦然盛开盛邀全城赏鉴项目地址：青岛·平度一中西侧电话：8867 8888公益广告总   编/綦   霏副总编/张泉水  杨江涛编   辑/山东省平度市新闻中心全媒体技术总监/宋嘉山联系电话/(0532)88321086\\\\n                \\\",\\\"Author\\\":\\\"掌上平度\\\",\\\"From\\\":null,\\\"Time\\\":1533711728000,\\\"Images\\\":12,\\\"ImageUrl\\\":\\\"https://mmbiz.qpic.cn/mmbiz/xP5v4lRAOibHdLIGXm8nU9xB7UIV2aib43Qw4B74bTPoygK9TWq58qYBdvydMfc2ErzAxDkfE0rpFl1GzMicDEpqw/640?wx_fmt=gif|https://mmbiz.qpic.cn/mmbiz_png/TEicYyckKpkd14vNspmqjribdjLIkuOs5bV7azL97NiaBoeK7cd5bzpaH5uk1wBLBQhMJYxHpkoTh8a6M2LCia4xibw/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_png/TEicYyckKpkcEhnn1bY5fUxxfiaD3YiapJFLBS49F19CD9Ohnl8W2JBhBIuAnFqicqQ5zRl0A1Lgjen3y2ECyPGibJw/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_png/TEicYyckKpkd14vNspmqjribdjLIkuOs5bhkpb2R3GOfTJg01H35Jp7U56Hbh6J46O0S9LScNvNOL6rzzuYnCL8g/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_jpg/TEicYyckKpkcEhnn1bY5fUxxfiaD3YiapJFXGI6dlo9YNYRdeaxXDuic3bKErgxN8ddDxHEaUJbyu4A4stXlRz0VCw/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/TEicYyckKpkd14vNspmqjribdjLIkuOs5b79AtgSftSTUlByLwfdorjNn8iaibAk9PqReDyibvIVicWribbtKNBBeT02Q/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_gif/TEicYyckKpkd14vNspmqjribdjLIkuOs5b4hWgH18OQwGEHE81lugtmhvfbSaZzwRp6dPicn20qdzlAykFia4WKNgA/640?wx_fmt=gif|https://mmbiz.qpic.cn/mmbiz_jpg/TEicYyckKpkd14vNspmqjribdjLIkuOs5bEWia1f6vPO3nib1gLzicKluorickaibNwibKD0STia6h32QZyF3IVriaNOibGBg/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/76CPRCM3dvXQboybY4X79fQZlz075HKQEXJu9jTsTAoMfcbvj4ghJnMiaCJKBRcnmRq2NpNERaVpwvnbBfhcHVw/640?wx_fmt=jpeg|http://mmsns.qpic.cn/mmsns/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakiazCJgcsXxj4oibzBEMlSibJA/0?wx_fmt=png|http://mmsns.qpic.cn/mmsns/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakujLlDWkMicRHmDenu2z36rQ/0?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakkiafMmGRWPCsIPeicHfibclVFrhJKiczLiaW30VWGZBVOM73URBWicgzNb4A/640?wx_fmt=jpeg\\\",\\\"Views\\\":0,\\\"Praises\\\":0,\\\"Place\\\":null,\\\"Person\\\":null,\\\"Keyword\\\":null,\\\"Hash\\\":\\\"\\\",\\\"ParagraphHash\\\":\\\"\\\",\\\"TopicID\\\":0,\\\"AddOn\\\":1533716587000,\\\"TitleSegment\\\":null,\\\"DefinedSite\\\":null,\\\"CustomerID\\\":\\\"\\\",\\\"Account\\\":\\\"zspd0532\\\",\\\"Pure\\\":null,\\\"Pureadj\\\":null,\\\"IsOriginal\\\":false,\\\"OriginalUrl\\\":\\\"\\\",\\\"IsHeadline\\\":false,\\\"Departments\\\":null,\\\"Companies\\\":null,\\\"Brands\\\":null,\\\"newsContent\\\":null,\\\"Tags\\\":null,\\\"IsGarbage\\\":0,\\\"Positive\\\":0,\\\"Negative\\\":0}\"},{\"headers\":{\"topic\":\"datacenter\",\"ip\":\"115.231.251.252:26016|60.190.238.168:38015\",\"key\":\"c60590169560c5c382bbfbf97522debd\",\"timestamp\":1533716589152},\"body\":\"{\\\"ID\\\":\\\"c60590169560c5c382bbfbf97522debd\\\",\\\"TaskID\\\":\\\"51825712\\\",\\\"TaskName\\\":\\\"微信_掌上平度\\\",\\\"AccountID\\\":\\\"51825712\\\",\\\"GroupName\\\":\\\"微信\\\",\\\"SiteID\\\":51825712,\\\"Language\\\":1,\\\"Channel\\\":20,\\\"Url\\\":\\\"http://mp.datacenter.qq.com/s?timestamp=1533716578&src=3&ver=1&signature=tgSlOV8*FQ08pfmNjh8ge4c8FQsssKhoopUphbmfTvAOSft-XdiSBbah5Vfg5L73VR4aTAD8cCBOXkTPSX2V6Eddtn101zSOTYJXL3HekXPq--bD0TNzHmRs0e9LJoUOwmI3DcdusIo1bSWuEWNjM7oBZLq2zUIdlpvDGdulTgc=\\\",\\\"Title\\\":\\\"【圣水浮金】平度被世界瞩目！青岛啤酒圣水浮金狂欢节暨首届龙虾节，8月10日盛大开幕！\\\",\\\"Content\\\":\\\"\\\\n                    \\\\n\\\\n                    \\\\n\\\\n                    \\\\n                    \\\\n                    2018精彩中国斥资百万打造2018青岛啤酒圣水浮金狂欢节暨首届龙虾节！8月10日盛大开幕只要您手握此消息，即可享受超级福利（领取方式见下文）激情盛典，万人狂欢夏日激情，一触即发8月10日起至19日，18:00—22:00来一起品尝美酒哦~更有各类特色美食映衬其中！先来领取您的活动专属福利吧★★★★★超级福利福利一，啤酒节入场券免费送：   只要您随手一晒盆友圈3天，让更多的友人知道，即可在8月10日至19日，凭此消息到现场服务区领取。福利二，梦幻灯光恐龙园入场券免费送：  只要您随手一晒盆友圈3天，让更多的友人知道，即可在8月10日至19日，凭此消息到现场服务区领取。福利三，冰爽啤酒送送送：购一张啤酒节门票，奖青岛扎啤一扎，并奖灯光恐龙园入场券1张，多买多送！注：具体怎么晒，请看底部第一条评论速度和家人朋友们参与进来吧~约 起 来       中国   平度       2018青岛啤酒圣水浮金狂欢节暨首届龙虾节高品质的“游玩盛会”高规格的“城市经典”▼8月10日-19日时间：2018年8月10日至8月19日地址：平度市圣水浮金公园（平度汽车东站309国道南城东埠村南）圣水浮金公园已成功举办5届青岛国际啤酒节平度会场，本届的青岛啤酒圣水浮金狂欢节暨首届龙虾节，主办方巨资力邀来自俄罗斯的天鹅歌舞团，奉上精彩激情的文艺演出。时间将定格在公元2018年8月10日，成吨小龙虾空降平度市！同时主办方引进环球金牌小吃，让大家品味舌尖上的万国风情！约约约~ 品尝美味小龙虾的同时  青岛扎啤、原浆扎啤供君“嗨啤”起来！ 圣水浮金灯光恐龙园，尽情玩乐圣水浮金八仙洞全面开放如此高大上的活动，怎能少得了嘉年华各种嘉年华项目等你来体验是不是好久没有玩过碰碰车了更有国内首个品牌网红美食团队，进驻下面给大家介绍一下啦，流口水吧！老萧家的肉卷▽▼▽老上海滩的品牌，老萧家祖传秘方，肉卷更有味！阿强煎的鸡蛋▽▼▽伦敦中国美食节创新大奖：阿强煎的蛋蛋红烧肉糖葫芦▽▼▽对，你没看错，红烧肉＋冰糖葫芦，不一样的创意~！更多品牌美食将在8月10日-19日精彩上线~管MAMA·茶、大个烤鱿鱼、杜爸爸·铁板蚵仔···外地人都赶来了，作为一个爱吃爱玩的平度人，你还不赶紧约起来？说到这里小编都迫不及待想去参加了！啤酒狂欢／网红美食荟谁借一位帅哥陪我去呀！重要的事情再说一遍！领福利！福利一，啤酒节入场券免费送：   只要您随手一晒盆友圈3天，让更多的友人知道，即可在8月10日至19日，凭此消息到现场服务区领取。福利二，梦幻灯光恐龙园入场券免费送：  只要您随手一晒盆友圈3天，让更多的友人知道，即可在8月10日至19日，凭此消息到现场服务区领取。福利三，冰爽啤酒送送送：购一张啤酒节门票，奖青岛扎啤一扎，并奖灯光恐龙园入场券1张，多买多送！注：具体怎么晒，请看底部第一条评论附：2018青岛啤酒圣水浮金狂欢节暨首届龙虾节攻略盛会时间：8月10日--8月19日营业时间：下午18:00-晚上22:00盛会地址：平度圣水浮金公园（平度汽车东站城东埠村南）自驾线路：自驾者导航到“圣水浮金公园”即可。如果链接失效，请不要惊慌，之前的记录仍然有效！记住时间、地点直接前往即可！如有任何疑问，请联系（时间：9:00——18:00)咨询热线：13105192297招商热线：17096252222公益广告总   编/綦   霏副总编/张泉水  杨江涛编   辑/山东省平度市新闻中心全媒体技术总监/宋嘉山联系电话/(0532)88321086\\\\n                \\\",\\\"Author\\\":\\\"掌上平度\\\",\\\"From\\\":null,\\\"Time\\\":1533711728000,\\\"Images\\\":31,\\\"ImageUrl\\\":\\\"https://mmbiz.qpic.cn/mmbiz/xP5v4lRAOibHdLIGXm8nU9xB7UIV2aib43Qw4B74bTPoygK9TWq58qYBdvydMfc2ErzAxDkfE0rpFl1GzMicDEpqw/640?wx_fmt=gif|https://mmbiz.qpic.cn/mmbiz_png/fgnkxfGnnkSibKL2ic1fkWU1orlibQ7IEaSg2MVFiaB0XWSJVJRTlTWMk5d8QLSfwFTcv1Hz06DncKjNM319snrrJA/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_gif/AfGVyYYbYuDw8EtnICicKeGia8buiafOpW4A062zWIoibdLs1RZgCgQvXkMexSv34DIRcZ7TvBQiaU6ro78aN7JgEnA/640?wx_fmt=gif|https://mmbiz.qpic.cn/mmbiz_jpg/AfGVyYYbYuDw8EtnICicKeGia8buiafOpW4MwGOdIYodHNZyj7MughHe5WXCLnKJxu08VeRV310LYcArqyKLkVACg/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/ibYHmsq1oJJG9u6eHicR4aA9mCdzUgZcJ05nMPQSXPI2o6J0pe1QCo1xaHU62Sibfgic0J68NwOCmtT0icybqwiaU94Q/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/AfGVyYYbYuDw8EtnICicKeGia8buiafOpW4I1bm2qObEt6fUbFIpBemjiaa6DKuwQELo3FI61kyXKSqCNibQrr3QDYw/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_gif/3q8XxPUtPvkw4QolcAGibuWDyAIoox2xV0cjIvx41BjB6LJjhsWRc31xYewYu9ia01kTutd3DaQhfqibE3w3q8c1Q/640?wx_fmt=gif|https://mmbiz.qpic.cn/mmbiz_jpg/ibYHmsq1oJJG9u6eHicR4aA9mCdzUgZcJ0YQvGwPaFsCpKFsRznmFWJES16wLrk5v3vlh2Kz6V2Z2uvoX5Kdrn9Q/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/ibYHmsq1oJJG9u6eHicR4aA9mCdzUgZcJ02soLUAuUa6ibRnYwEAsDtjNnRnFLtEkJnSkZeTsiaRQLESGHQftYibiadg/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/6EqZaxxYNGnIKBNJQ3TWy3nyVbUkNFTfn9hvPNLjfrN5lFk9Gc1JH5jmXMjia3aud1rCibMPcUoian2UFye8ZVtDg/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_png/6EqZaxxYNGl8Tx8vuibicL4LSbqZXzFwQkrzu6CRlBb22ECfHBVUoxO8u1B8bDX5zcZ0qlT8zpkKibgmwYYZWykVg/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_gif/1hLoLExqs9h2V6mIMYacXyf26DQmGHZupSFR2cc7x4erB9KesRib83vGOrmSuw5WmJ1BnzAjFFOOSIjpcxJgPZw/640?wx_fmt=gif|https://mmbiz.qpic.cn/mmbiz_jpg/ibYHmsq1oJJG9u6eHicR4aA9mCdzUgZcJ0dykagdp7OIWgT4iaVmOHcv8Ayt5jcHT5oPlQJ6K5R1Dr7VbkDFr8aiaA/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/ibYHmsq1oJJG9u6eHicR4aA9mCdzUgZcJ0BYRTUF2uG1r6YvZ0Kv1XauBPr6Fn2Ewt31cgBR61sTMIibYeSKjibPEA/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_png/ibYHmsq1oJJG9u6eHicR4aA9mCdzUgZcJ0nf5Y8mUWGniaqiaGuwWR366PBPo8a49K0aricllaobpqBf42CicbAfdGEQ/640?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_jpg/ibYHmsq1oJJG9u6eHicR4aA9mCdzUgZcJ0shYJolEqUgiaoBsTPMGRxicc0zibfOzbK0al4USNdg1luf1q4IsfgUk4Q/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/ibYHmsq1oJJG9u6eHicR4aA9mCdzUgZcJ0VnbFlCA8t4vUhBNq8Wbn0IanJd5G70hjicSO5pBWScFA65PK09U3DMA/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_png/bunMTAibeSE7d5To1yAeaUvWb4oQroOM117m0JJucibBv64icmlKACRJsJyqo0ryibJJ1B8tsibAFodev30qYdbeiazQ/640.png?|https://mmbiz.qpic.cn/mmbiz_jpg/PsLmb0ibibTzQjfoNyI1kEiaVhS2mvKKCgd8M1IPf54P4fVAjCicjNWskfaYMgMX7PrYXU6qpicqia6eMJ329z0LGl7g/640?|https://mmbiz.qpic.cn/mmbiz_jpg/PsLmb0ibibTzTUro3FCyNTaiaIaMicExKFJBuUmDibDbtf0WsHaFgpR9bY7Q9AmIw8iclnq0If0QhliaFrxCIiaWeKYnlQ/640?|https://mmbiz.qpic.cn/mmbiz_jpg/BgnEV4oKJdKjxj5UFr0mgzhmSka1xUoBDTfM9oYIh80DrjAHyFbTrsq97VhQiax57ff97xH9fsNgcwezVwNRfyw/640?|https://mmbiz.qpic.cn/mmbiz_png/PsLmb0ibibTzTUro3FCyNTaiaIaMicExKFJByJRbjn0n2pDhrPgZnOcj9uYIhU3NVuLOmUHPoOjMXwTQ16nCPbOzJw/640?|https://mmbiz.qpic.cn/mmbiz_png/ibFcljb71VmI6y5qzqHbvt140HM44sLgXHv0QUsK8UPXmzSbH6OLyNThlDGOB5c4dvUjrukPCMqBjmeaG4yClqg/640?|https://mmbiz.qpic.cn/mmbiz_png/ibFcljb71VmI6y5qzqHbvt140HM44sLgX4LTiaB8BIxK9HiagftwfVqEkM2hIq9WjQYoyLdumN0Lt1rSsGSPjzH1A/640?|https://mmbiz.qpic.cn/mmbiz_gif/4BY4nn87ITkYibXSrg4akQicFianNJCG2W3iaKXPXwZkxWQF5Dth5XkjRDxFr7coiajCXeKoKL1jqLT501iazy11pxXw/640?|https://mmbiz.qpic.cn/mmbiz/cZV2hRpuAPjOjIEA1OjSicXHcia9Mj9RQjHyzPCqX3VQptpicRevvzd6fCvKjeYKvic7KJSQasYOmoP6V6oTAWJuRg/640?|https://mmbiz.qpic.cn/mmbiz_jpg/AfGVyYYbYuBuutPyKtSoZ3ZW7GHlOfZ6egI9JNDIvzamaIUKGzA2e8Z2fSRbUU3N5AXAtTCT3XkdPy51uK2lNw/640?wx_fmt=jpeg|https://mmbiz.qpic.cn/mmbiz_jpg/76CPRCM3dvUoHzCdqSiaibRXsCKYWLOmVQ3I9YLDOvnOGVYakqT23wLR5gaapNukCLUImnEfiapkptyiaz5CmzUZ9w/640?wx_fmt=jpeg|http://mmsns.qpic.cn/mmsns/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakiazCJgcsXxj4oibzBEMlSibJA/0?wx_fmt=png|http://mmsns.qpic.cn/mmsns/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakujLlDWkMicRHmDenu2z36rQ/0?wx_fmt=png|https://mmbiz.qpic.cn/mmbiz_jpg/xP5v4lRAOibHTJYbMSO6sChwaMoWoaFakkiafMmGRWPCsIPeicHfibclVFrhJKiczLiaW30VWGZBVOM73URBWicgzNb4A/640?wx_fmt=jpeg\\\",\\\"Views\\\":0,\\\"Praises\\\":0,\\\"Place\\\":null,\\\"Person\\\":null,\\\"Keyword\\\":null,\\\"Hash\\\":\\\"\\\",\\\"ParagraphHash\\\":\\\"\\\",\\\"TopicID\\\":0,\\\"AddOn\\\":1533716589000,\\\"TitleSegment\\\":null,\\\"DefinedSite\\\":null,\\\"CustomerID\\\":\\\"\\\",\\\"Account\\\":\\\"zspd0532\\\",\\\"Pure\\\":null,\\\"Pureadj\\\":null,\\\"IsOriginal\\\":false,\\\"OriginalUrl\\\":\\\"\\\",\\\"IsHeadline\\\":false,\\\"Departments\\\":null,\\\"Companies\\\":null,\\\"Brands\\\":null,\\\"newsContent\\\":null,\\\"Tags\\\":null,\\\"IsGarbage\\\":0,\\\"Positive\\\":0,\\\"Negative\\\":0}\"}]"
    }
]
        public_divs = self.driver.find_elements_by_css_selector('.clearfix.list_query')
        for public_div in public_divs:
            if '提交入库' not in public_div.text:
                # 点击进入公众号
                gxh = public_div.find_element_by_id('nickname')
                gxh.click()
                time.sleep(2)

                all_handles = self.driver.window_handles  # 获取到当前所有的句柄,所有的句柄存放在列表当中
                '''获取非最初打开页面的句柄'''
                if len(all_handles) > 1:
                    # for index, handles in enumerate(all_handles):
                    #     if index == 1:
                    self.driver.switch_to.window(all_handles[1])
                    time.sleep(0.5)

                    # 获取公众号 ID, 名称, 微信号
                    account = Acount()
                    account.name = self.driver.find_element_by_class_name('fs22').text

                    wx_num = self.driver.find_element_by_class_name('info-li').text.split('\n')[0]
                    account.wx_account = wx_num.split("：")[-1]
                    get_account_id_url = 'http://60.190.238.178:38010/search/common/wxaccount/select?token=9ef358ed-b766-4eb3-8fde-a0ccf84659db&account={}'.format(
                        account.wx_account)
                    url_resp = requests.get(get_account_id_url)
                    json_obj = json.loads(url_resp.text)
                    results = json_obj.get('results')
                    account.account_id = ''
                    for i in results:
                        account.account_id = i.get('AccountID')
                        break

                    for i in range(2):
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(0.5)
                    # 得到所有文章并解析
                    data_all = self.driver.find_elements_by_css_selector('.wxDetail.bgff')
                    datas = data_all[-1]
                    items = datas.find_elements_by_class_name('clearfix')
                    for count, item in enumerate(items):
                        if count == 0:
                            continue
                        url = item.find_element_by_tag_name('a').get_attribute('href')
                        title = item.find_element_by_class_name('cr30').text
                        read_num = item.find_element_by_css_selector('.wxAti-info').find_element_by_tag_name(
                            'span').text
                        praise_num = \
                        (item.find_element_by_css_selector('.wxAti-info').find_elements_by_tag_name('span'))[-1].text
                        article_time = item.find_element_by_class_name('fr').text
                        log(name, read_num, praise_num)
                        save_all = {
                            'url': url,
                             'read_num': read_num,
                            'praise_num': praise_num,
                            'title': title,
                            'public_url': self.driver.current_url,
                            'insert_time': datetime.datetime.now()
                        }
                        parsed_url = urllib.parse.quote(url)
                        upload_url = 'http://183.131.241.60:38011/InsetUrl?url={}&views={}&praises={}'.format(
                            parsed_url, read_num, praise_num)
                        requests.get(upload_url)
                        cursor.execute(
                            "INSERT INTO wechat_qingbo_copy(current_url, article_url, read_num, praise_num, insert_time) VALUES (%s, %s, %s, %s, %s)",
                            (self.driver.current_url, url, read_num, praise_num, datetime.datetime.now()))
                        db.commit()

                        # 文章解析
                        article = Article()
                        resp = requests.get(url)
                        e = pq(resp.text)
                        # account = e("#js_name")
                        article_content = e("#js_content").text()
                        # article_author = e("")

                        article.url = url
                        article.title = title
                        article.content = article_content
                        article.author = account.wx_account
                        article.From = account.wx_account
                        article.time = self.date_to_timestamp(article_time)

                        send_content = JsonEntity(article, account)



                        # urun['read_praise_num_details_temp'].insert(save_all)

                    self.driver.close()
                    # for index, handles in enumerate(all_handles):
                    #     if index == 0:
                    self.driver.switch_to.window(all_handles[0])
            else:
                log('not found available public')
                return 'not found'

    def run(self):
        self.login_website()
        count = 0
        while True:
            try:
                log('request count {}'.format(count))
                self.name_list = self.get_public_name()
                for name in self.name_list:
                    try:
                        log('start name {}'.format(name))
                        self.get_numb(name, count)
                    except Exception as e:
                        log(e)
                        if 'timeout' in str(e):
                            self.driver.get('http://www.gsdata.cn/query/wx?q=%E5%BC%80%E8%AF%9A%E5%BF%AB%E5%8D%B0')
                            time.sleep(1)
                    count += 1
                time.sleep(3)
                count += 1
            except Exception as e:
                log('error afsdfadfsd')
                if self.driver is not None:
                    log(self.driver.current_url)
                    self.driver.quit()
                self.driver = self.get_driver()
                self.login_website()
                count += 1
                continue
        print('haha')


if __name__ == '__main__':
    test = PublicDetails()
    test.run()
