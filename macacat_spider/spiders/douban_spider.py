# -*- coding: utf-8 -*-
import scrapy
from macacat_spider.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['douban.com']
    # 入口地址
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']/ol[@class='grid_view']/li")
        for list_item in movie_list:
            douban_item = DoubanItem()
            douban_item['serial_number'] = list_item.xpath(".//div[@class='item']/div[@class='pic']/em/text()").extract_first()
            douban_item['movie_name'] = list_item.xpath("./div[@class='item']/div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()

            introduce_content = list_item.xpath("./div[@class='item']/div[@class='info']/div[@class='bd']/p[1]/text()").extract()
            content = ''
            for i_content in introduce_content:
                content += ''.join(i_content.split())

            douban_item['introduce'] = content
            douban_item['star'] = list_item.xpath("./div[@class='item']/div[@class='info']/div[@class='bd']/div[@class='star']/span[2]/text()").extract_first()
            douban_item['evaluate'] = list_item.xpath("./div[@class='item']/div[@class='info']/div[@class='bd']/div[@class='star']/span[4]/text()").extract_first()
            douban_item['describe'] = list_item.xpath("./div[@class='item']/div[@class='info']/div[@class='bd']/p[@class='quote']/span[@class='inq']/text()").extract_first()
            # print(douban_item)
            yield douban_item
        next_page_url = response.xpath("//div[@class='paginator']/span[@class='next']/a/@href").extract_first()
        if next_page_url is not None:
            # next_page_url = response.urljoin(next_page_url)
            # yield scrapy.Request(next_page_url, callback=self.parse)
            # response.follow()可以代替上面兩句
            yield response.follow(next_page_url, callback=self.parse)