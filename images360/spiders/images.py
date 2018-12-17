# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Spider,Request
from urllib.parse import urlencode
from images360.items import Images360Item


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        data = {'ch':'photography','listtype':'new','temp':1}
        base_url = 'http://images.so.com/zj?'
        for page in range(1,self.settings.get('MAX_PAGE') + 1):
            data['sn'] = page * 30
            params = urlencode(data)
            url = base_url + params
            yield Request(url,self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = Images360Item()
            item['id'] = image.get('index')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('group_title')
            item['thumb'] = image.get('qhimg_thumb_url')
            yield item
