# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import os
from i4 import settings

class I4Pipeline(object):
    def process_item(self, item, spider):
		if item['link'] and item['desc'] and item['title']:
			dir_name = item['title'].encode('gbk')
			dir_path = '{0}/{1}/{2}'.format(settings.IMAGE_STORE, settings.BOT_NAME, dir_name)
			if not os.path.exists(dir_path):
				os.makedirs(dir_path)

			image_url = item['link']
			image_name = ''.join(image_url.split('/')[3:])
			file_path = '{0}/{1}'.format(dir_path, image_name)

			if os.path.exists(file_path):
				return item

			with open(file_path, 'wb') as f:
				resp = requests.get(image_url, stream=True)
				f.write(resp.content)


		return item
			
