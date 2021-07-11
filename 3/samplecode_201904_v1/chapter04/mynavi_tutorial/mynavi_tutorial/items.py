# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MynaviTutorialItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    image_url = scrapy.Field()
    genre = scrapy.Field()
    body = scrapy.Field()
