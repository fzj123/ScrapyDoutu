# -*- coding: utf-8 -*-
import os
import scrapy
import requests
from ScrapyDoutu.items import ScrapydoutuItem
import logging

class DoutulaSpider(scrapy.Spider):
    name = "doutu"
    allowed_domains = ["doutula.com", "sinaimg.cn"]
    start_urls = ['https://www.doutula.com/photo/list/?page={}'.format(i) for i in range(1, 2200)] # 我们暂且爬取40页图片

    def parse(self, response):
        i = 0
        #//*[@id="pic-detail"]/div/div[3]/div[2]/ul/li/div/div/a
        for content_img in response.xpath('//*[@id="pic-detail"]/div/div[3]/div[2]/ul/li/div/div/a'):
            i += 1
            item = ScrapydoutuItem()
            item['img_url'] = content_img.xpath('//img/@data-original').extract()[i]
            item['name'] = content_img.xpath('//p/text()').extract()[i]
            try:
                if not os.path.exists('doutu'):
                    print("aaa")
                    print('路径信息' + str(os.path.exists('doutu')))
                    os.makedirs('doutu')
                r = requests.get(item['img_url'])
                print(r)
                suffix = str(item['img_url']);

                if suffix.__contains__('!dta'):
                    suffix = suffix[-8:-4]
                # filename = 'doutu\\{}'.format(item['name']) + item['img_url'][-4:]
                filename = 'doutu\\{}'.format(item['name']) + suffix
                with open(filename, 'wb') as fo:
                    fo.write(r.content)

            except:
                print('有问题爬取的数据！！！')
            yield item