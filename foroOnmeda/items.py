# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class forosOnmedaSpyder(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    forum_url = scrapy.Field()
    forum_title = scrapy.Field()
    forum_text = scrapy.Field()
    subject_url = scrapy.Field()
    subject_title = scrapy.Field()
    subject_user = scrapy.Field()
    post_user = scrapy.Field()
    post_member_group = scrapy.Field()
    post_date = scrapy.Field()
    post_count = scrapy.Field()
    post_text = scrapy.Field()
    user_url = scrapy.Field()
    user_location = scrapy.Field()
    user_date_registered = scrapy.Field()
    pass
