# -*- coding: utf-8 -*-

import scrapy
from i4.items import I4Item

class I4Spider(scrapy.Spider):
	name = 'I4'
	start_urls = [
		'http://www.aitaotu.com/guonei/1611.html',
		'http://www.aitaotu.com/guonei/1644.html',
	]
	allow_domains = ['www.aitaotu.com']

	def parse(self, response):
		links = response.xpath('//*[@id="big-pic"]/p/a/img/@src').extract()
		descs = response.xpath('//*[@id="big-pic"]/p/a/img/@alt').extract()
		title = response.xpath('//*[@id="photos"]/h2/text()').extract()

		item = I4Item()
		item['title'] = title[0]
		item_dict = dict(zip(descs, links))
		
		for desc, link in item_dict.items():
			item['desc'] = desc
			item['link'] = link
			yield item

		next_page_relative = response.xpath('//*[@id="nl"]/a/@href').extract()[0]

		try:
			next_page = response.urljoin(next_page_relative)
			yield scrapy.Request(next_page, callback = self.parse)
		except Exception, e:
			print Exception, ":", e
		
