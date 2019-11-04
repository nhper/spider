# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import ShangbiaoItem

class ShangbiaowangSpider(scrapy.Spider):
    name = 'shangbiaowang'
    def start_requests(self):
        url = 'http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearchDG.html'
        annNum = 1
        while True:
            data = {
                'page': '1',
                'rows': '1000000',
                'annNum': str(annNum),
                'annType': '',
                'tmType': '',
                'coowner': '',
                'recUserName': '',
                'allowUserName': '',
                'byAllowUserName': '',
                'appId': '',
                'appIdZhiquan': '',
                'bfchangedAgengedName': '',
                'changeLastName': '',
                'transferUserName': '',
                'acceptUserName': '',
                'regName': '',
                'tmName': '',
                'intCls': '',
                'fileType': '',
                'totalYOrN': 'false',
                'appDateBegin': '',
                'appDateEnd': '',
                'agentName': '',
            }
            annNum+=1
            yield scrapy.FormRequest(url=url,formdata=data)
    def parse(self, response):
        item = ShangbiaoItem()
        item['content']=[]
        res = json.loads(response.text)['rows']
        for i in res:
            x=[i['reg_num'],i['reg_name'],i['tmname']]
            item['content'].append(x)
        yield item
