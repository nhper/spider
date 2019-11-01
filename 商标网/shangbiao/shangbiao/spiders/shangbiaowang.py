# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import ShangbiaoItem

class ShangbiaowangSpider(scrapy.Spider):
    name = 'shangbiaowang'
    def start_requests(self):
        url = 'http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearchDG.html'
        data = {
            'page': '1',
            'rows': '1000',
            'annNum': '1669',
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
        while int(data['page'])<310:
            yield scrapy.FormRequest(url=url,formdata=data)
            data['page']=str(int(data['page'])+1)
    def parse(self, response):
        item = ShangbiaoItem()
        item['content']=[]
        res = json.loads(response.text)['rows']
        for i in res:
            x=[i['reg_num'],i['reg_name'],i['tmname']]
            item['content'].append(x)
        yield item
