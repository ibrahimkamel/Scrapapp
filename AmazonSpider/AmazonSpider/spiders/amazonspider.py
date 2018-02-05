# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from AmazonSpider.items import AmazonspiderItem,AmazonspiderMetaData
from scrapy.loader import ItemLoader
from scrapy.conf import settings

class AmazonspiderSpider(scrapy.Spider):
	name = 'amazonspider'
	allowed_domains = ['amazon.com']
	start_urls = ['https://www.amazon.com/Amazon-Echo-Dot-Portable-Bluetooth-Speaker-with-Alexa-Black/dp/B01DFKC2SO/',
				'https://www.amazon.com/Bose-SoundLink-Bluetooth-Discontinued-Manufacturer/dp/B00D5Q75RC/',
				'https://www.amazon.com/Belker-Headphone-Adapter-Connector-Microphone/dp/B071YDG983/']
	

	def __init__(self, *args, **kwargs):
		# self.domain = kwargs.get('domain')
		self.start_urls = [kwargs.get('url','https://www.amazon.com/Belker-Headphone-Adapter-Connector-Microphone/dp/B071YDG983/')]
		# self.start_urls = urls
		
		self.unique_id = settings['unique_id']
		print("==============")
		print(self.unique_id)
		print("==============")
		super(AmazonspiderSpider, self).__init__(*args, **kwargs)

	def parse(self, response):
		# name = response.xpath('//span[@id="productTitle"]/text()').extract_first()
		# price = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract()
		# if not price:
		# 	price = response.xpath('//span[@id="priceblock_dealprice"]/text()').extract()
					
		# description = response.xpath('//div[@id="productDescription"]/p/text()').extract()
		# seller = response.xpath('//a[@id="bylineInfo"]/text()').extract()
		name = response.xpath('normalize-space(//div[@id="titleSection"]/.//span/text())').extract_first()
		# name = name.strip()
		platform = "Amazon"
		seller = response.xpath('normalize-space(//div[@data-feature-name="bylineInfo"]/.//a/text())').extract_first()
		if not seller:
			seller = response.xpath('normalize-space(//div[@data-feature-name="brandByline"]/.//a/text())').extract_first()
		# seller = seller.strip()
		url = response.request.url
		timestamp = datetime.utcnow()
		metadata = {}
		price = response.xpath('//div[@id="price"]/.//span[contains(@class,"a-color-price")]/text()').extract_first()
		review = response.xpath('//div[@id="averageCustomerReviews"]/.//span[contains(@class,"reviewCountTextLinkedHistogram")]/@title').extract_first()
		review = response.xpath('normalize-space(//i[contains(@class,"averageStarRating")]/span/text())').extract_first()
		review = review.split(" out ")[0]
		num_of_reviews = response.xpath('normalize-space(//span[contains(@class,"totalReviewCount")]/text())').extract_first()
		descriptions = response.xpath('normalize-space(//div[@id="feature-bullets"]/.//span/text())').extract()
		# for description in descriptions:
		# 	description = description.strip()
		# metadata['name'] = name
		# metadata['seller'] = seller
		# metadata['Description'] = description
		# metadata['review'] = review
		# metadata['num_of_reviews'] = num_of_reviews
		# metadata['price'] = price



		l = ItemLoader(item=AmazonspiderItem(),response=response)
		l2 = ItemLoader(item=AmazonspiderMetaData(),response=response)


		
		l.add_value("platform",platform)
		l.add_value("timestamp",timestamp)
		l.add_value("url",url)
		l.add_value("unique_id",self.unique_id)
		
		
		l2.add_value("name",name)
		l2.add_value("seller",seller)
		l2.add_value("Description",descriptions)
		l2.add_value("review",review)
		l2.add_value("num_of_reviews",num_of_reviews)
		l2.add_value("price",price)


		l.add_value("metadata",l2.load_item())


		return l.load_item()
