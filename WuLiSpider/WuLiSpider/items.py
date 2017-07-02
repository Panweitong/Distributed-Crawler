# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WulispiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JsGoodsItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    date = scrapy.Field()
    remark = scrapy.Field()
    store = scrapy.Field()
    storeUrl = scrapy.Field()
    comments = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
            insert into jd_goods(id, name, url, price, remark, date,store,storeUrl,comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE price=VALUES(price), date=VALUES(date)
        """
        params = (self["id"], self["name"], self["url"], self["price"], self["remark"], self["date"], self["store"], self["storeUrl"], self["comments"])
        return insert_sql, params


class NewsItem(scrapy.Item):
    # id = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
            insert into news_content(title, source, url, content, date) VALUES ( %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), date=VALUES(date)
        """
        params = (self["title"], self["source"], self["url"], self["content"], self["date"])
        return insert_sql, params