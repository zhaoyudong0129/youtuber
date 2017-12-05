# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from youtuber.items import YoutuberLoader, YoutuberItem
from youtuber.utils.common import get_md5


class YoutubeSpider(RedisSpider):
    name = 'youtube'
    allowed_domains = ['www.youtube.com']
    redis_key = 'youtube:start_urls'
    start_urls = ['https://www.youtube.com/user/PhoneBunch/about']
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'

    def __init__(self, **kwargs):
        # 每个爬虫绑定一个web driver,降低资源消耗, 与middleware解耦
        # self.browser = webdriver.Chrome(executable_path='/Users/zyd/Downloads/chromedriver')
        self.browser = webdriver.PhantomJS(
            executable_path='/Users/zyd/Downloads/phantomjs-2.1.1-macosx 2/bin/phantomjs')
        # 释放资源
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        super(YoutubeSpider, self).__init__(**kwargs)

    def parse(self, response):
        item_loader = YoutuberLoader(YoutuberItem(), response)
        # youtube个人档案页提取规则 chrome
        # item_loader.add_css('email', '#description-container', re='([A-Za-z0-9-_]*@[A-Za-z0-9-_.]*)')
        # item_loader.add_css('name', '#channel-title::text')
        # item_loader.add_css('subscriber_count', '#subscriber-count::text', re='([0-9,.]*)')
        # item_loader.add_css('register_date', '#right-column yt-formatted-string:nth-child(2)',re=r'(\d+年\d+月\d日)')
        # item_loader.add_css('view_count', '#right-column yt-formatted-string:nth-child(3)',re='([0-9,.]*)')
        #
        # item_loader.add_xpath('country','//*[@id="details-container"]/table/tbody/tr[2]/td[2]/yt-formatted-string/text()')

        # youtube个人档案页提取规则 ph
        item_loader.add_css('email', '.about-description pre::text', re='([A-Za-z0-9-_]*@[A-Za-z0-9-_.]*)')
        item_loader.add_css('name', '.branded-page-header-title-link::text')
        item_loader.add_css('subscriber_count', 'span.about-stat:nth-child(1) b::text')
        # item_loader.add_css('subscriber_count', 'span.about-stat:nth-child(1) b::text', re='([0-9,.]*)')
        item_loader.add_css('register_date', 'span.about-stat:nth-child(4)::text')
        # item_loader.add_css('register_date', 'span.about-stat:nth-child(4)::text', re=r'(\d+年\d+月\d+日)')
        item_loader.add_css('view_count', 'span.about-stat:nth-child(2) b::text')
        # item_loader.add_css('view_count', 'span.about-stat:nth-child(2) b::text', re='([0-9,.]*)')

        item_loader.add_css('country', '.country-inline::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('object_url_id', get_md5(response.url))

        item = item_loader.load_item()
        yield item

        # 深度优先策略
        # for PhantomJS
        links = response.css('a.yt-uix-tile-link::attr(href)').extract()

        # for chrome
        # links = response.css('a.ytd-mini-channel-renderer::attr(href)').extract()
        for link in links:
            yield scrapy.Request(url=response.urljoin(link) + '/about', callback=self.parse)

    def spider_closed(self, spider):
        '''
        爬虫扫尾工作
        :param spider:
        :return:
        '''
        self.browser.quit()
        # response.css('.branded-page-header-title-link::text').extract()
        # response.css('.about-description pre::text').extract()
        # response.css('span.about-stat:nth-child(1) b::text').extract()
        # response.css('span.about-stat:nth-child(2) b::text').extract()
        # response.css('span.about-stat:nth-child(4) b::text').extract()
        # response.css('.country-inline::text').extract()
