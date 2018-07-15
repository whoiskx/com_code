import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from dingdian.items import DingdianItem, DcontentItem


class DingDianSpider(scrapy.Spider):
    name = 'dingdian'
    allowed_domains = ['23wx.cc']
    bash_url = 'http://www.23wx.cc/class/'
    bashurl = '.html'

    def start_requests(self):
        # for i in range(11):
        #     url = self.bash_url + str(i) + '_1' + self.bashurl
        #     yield Request(url, self.parse)
        yield Request('http://www.23wx.cc/quanben/1', self.parse)

    def parse(self, response):
        # print(response.text)
        max_num = BeautifulSoup(response.text, 'lxml').find('div', class_='pagelink',).find_all('a')[-1].get_text()
        bashurl = str(response.url)[:-1]
        print(max_num, bashurl)
        max_num = 1
        for num in range(1, int(max_num)+1):
            url = bashurl + str(num)
            yield Request(url, callback=self.get_name, dont_filter=True)

    def get_name(self, response):
        tds = BeautifulSoup(response.text, 'lxml').find_all('tr')
        for count, td in enumerate(tds):
            if count == 0:
                continue
            novelname = td.find('a').get_text()
            noveurl = td.find('a')['href']
            author = td.find_all('td')[2].get_text()
            print(novelname, noveurl, author)
            if count > 3:
                break
            yield Request(noveurl, callback=self.get_chapterurl, meta={'name': novelname,
                                                                       'url': noveurl,
                                                                       'author': author,})

    def get_chapterurl(self, response):
        item = DingdianItem()
        item['name'] = response.meta['name']
        item['noveurl'] = response.meta['url']
        author = response.meta['author']

        category = BeautifulSoup(response.text, 'lxml').find('dd').get_text()
        name_id = str(item['noveurl'])[-6:-1]

        item['author'] = author
        item['category'] = category
        item['name_id'] = name_id

        yield item
        bash_urls = BeautifulSoup(response.text, 'lxml').find_all('dd')
        num = 0
        for count, initial_url in enumerate(bash_urls):
            if count > 6:
                break
            num += 1
            bash_url = item['noveurl'] + initial_url.find('a')['href']
            chapter_url = bash_url
            chapter_name = category
            print('afasdf', bash_url, chapter_name)
            yield Request(chapter_url, callback=self.get_chapter_content, meta={'num': num,
                                                                                'name_id': name_id,
                                                                                'chapter_name': chapter_name,
                                                                                'chapter_url': chapter_url,
                                                                                })
            # yield Request(bash_url, callback=self.get_chapter, meta={'name_id': name_id,})

    # def get_chapter(self, response):
    #     urls =
    #     num = 0
    #     for url in urls:
    #         num += 1
    #         chapter_url = response.url + url[0]
    #         chapter_name = url[1]
    #         yield Request(chapter_url, callback=self.get_chapter_content, meta={'num':num,
    #                                                                             'name_id': response.meta['name_id'],
    #                                                                             'chapter_name': chapter_name,
    #                                                                             'chapter_url': chapter_url,
    #                                                                             })

    def get_chapter_content(self, response):
        item = DcontentItem()
        item['num'] = response.meta['num']
        item['id_name'] = response.meta['name_id']
        item['chapter_name'] = response.meta['chapter_name']
        item['chapter_url'] = response.meta['chapter_url']
        content = BeautifulSoup(response.text, 'lxml').find(id='content').get_text()
        item['chapter_content'] = str(content).replace('\xa0', '')
        return item