# -*- coding: utf-8 -*-
import scrapy
import re
from  ..items import DyttItem
class DianyingttSpider(scrapy.Spider):
    name = 'dianyingtt'
    def start_requests(self):
        url = 'https://www.dy2018.com/'
        for i in range(21):
            nurl = url+str(i)+'/'
            yield scrapy.Request(nurl)

    def parse(self, response):
        page = response.xpath("//div[@class='x']/p/text()").getall()[0]
        p = int(re.findall("/(\d+)",page)[0])  # 匹配每一个分类的总页数
        urls = response.xpath("//b/a[2]/@href").getall()
        furl = 'https://www.dy2018.com'
        for url in urls:
            yield scrapy.Request(furl+url,callback=self.index)
        surl = response.url
        print(surl)
        if 'index' not in surl:
            for i in range(2,p+1):
                yield scrapy.Request(surl+"index_"+str(i)+".html")
    def index(self,response):
        con = DyttItem()
        try:
            name = response.xpath("//h1/text()").getall()[0]
            grade = response.xpath("//strong[@class='rank']/text()").getall()[0]
            type = "/".join(response.xpath("//div[@class='position']/span[2]/a/text()").getall())
            updatetime = response.xpath("//span[@class='updatetime']/text()").getall()[0].split('：')[1]
            img = response.xpath("//div[@id='Zoom']//img[1]/@src").getall()[0]
            downloadurl = response.xpath("//div[@id='Zoom']/table//a/text()").getall()
            con['content']={
                'name':name, # 电影名
                'grade':grade, # 评分
                'type':type, # 类型
                'updatetime':updatetime,  # 发布时间
                'imgurl':img, # 图片地址
                'downloadurl':downloadurl,  # 下载地址
            }
            yield con
        except Exception as  e:
            print('网页出错了----------------',e)