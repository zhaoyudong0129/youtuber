# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter, CsvItemExporter


class YoutuberPipeline(object):
    def process_item(self, item, spider):
        return item


# class CsvExporter(CsvItemExporter):
#     self.fields_to_export


class CSVExportPipeline(object):
    '''
    用scrapy 提供的exporter
    '''

    def __init__(self):
        pass

    def open_spider(self, spider):
        self.file = open('youtuber.csv', 'wb')
        # fields_to_export: set the order of fields
        # 如果想解耦，需要将item绑定spider
        self.exporter = CsvItemExporter(self.file,
                                        fields_to_export=['url', 'name', 'email', 'subscriber_count', 'view_count',
                                                          'country', 'register_date'])
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
