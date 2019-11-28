# -*- coding: utf-8 -*-
import scrapy
from ..items import LianjiaItem
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
}
class LiangaSpider(scrapy.Spider):
    name = 'lianga'
    def start_requests(self):
        for i in range(1,101):
            url = 'https://bj.lianjia.com/zufang/pg'+str(i)+'/'
            yield scrapy.Request(url,headers=headers)

    def parse(self, response):
        urls = response.xpath("//div[@class='content__list']/div/a/@href").getall()
        for url in urls:
            yield scrapy.Request('https://tj.lianjia.com'+url,headers=headers,callback=self.parse1)
    def parse1(self,response):
        item = LianjiaItem()
        title = response.xpath("//p[@class='content__title']/text()").getall()[0]
        class_code = response.xpath('//i[@class="house_code"]/text()').getall()[0]
        money = response.xpath("//p[@class='content__aside--title']/span/text()").getall()[0]
        size = response.xpath("//p[@class='content__article__table']/span[3]/text()").getall()[0]
        item['title']=title
        item['class_code']=class_code
        item['money']=money
        item['size']=size
        yield item