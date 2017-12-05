# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymysql
from scrapy.exporters import JsonItemExporter, CsvItemExporter
from twisted.enterprise import adbapi

logger = logging.getLogger(__name__)


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


class MysqlTwistPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)

        query.addErrback(self.handle_error, item)

    def handle_error(self, failure, item):
        logger.error(failure)
        logger.info(item.info())

    def do_insert(self, cursor, item):
        sql, params = item.get_insert_sql()

        cursor.execute(sql, params)

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(host=settings['MYSQL_HOST'],
                        db=settings['MYSQL_DB'],
                        user=settings['MYSQL_USER'],
                        password=settings['MYSQL_PASSWD'],
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor
                        )

        dbpool = adbapi.ConnectionPool("pymysql", **dbparams)

        return cls(dbpool)
