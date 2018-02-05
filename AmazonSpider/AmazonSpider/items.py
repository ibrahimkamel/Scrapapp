# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonspiderItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	# def __init__(self, unique_id, *args, **kwargs):
	# 	self.unique_id = unique_id
	# @classmethod
	# def from_crawler(cls, crawler):
	# 	return cls(
	# 		unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
	# 		)
	platform  = scrapy.Field()
	unique_id  = scrapy.Field()
	url = scrapy.Field()
	timestamp = scrapy.Field()
	metadata = scrapy.Field()


class AmazonspiderMetaData(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	name = scrapy.Field()
	seller = scrapy.Field()
	
	price = scrapy.Field()
	Description = scrapy.Field()
	review = scrapy.Field()
	num_of_reviews = scrapy.Field()
	