# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


class YoutuberLoader(ItemLoader):
    default_output_processor = TakeFirst()


class YoutuberItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field(input_processor=MapCompose(lambda x: x.strip()))
    email = scrapy.Field()
    subscriber_count = scrapy.Field()
    view_count = scrapy.Field()
    register_date = scrapy.Field()
    country = scrapy.Field(input_processor=MapCompose(lambda x: x.strip()))


if __name__ == '__main__':
    item_loader = YoutuberLoader(YoutuberItem())
    # youtube个人档案页提取规则
    item_loader.add_value('email', 'For Business Enquiries: technoreviewww@gmail.com',
                          re='([A-Za-z0-9-_]*@[A-Za-z0-9-_.]*)')
    item_loader.add_value('subscriber_count', '397,789 位订阅者 ', re='([0-9,.]*)')

    item = item_loader.load_item()

    print(item)
