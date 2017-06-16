# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy_spiders.items import ImdbItem, OnDvdItem
import re

# Need to deal with 's and : here and also in tmdb_posters
def clean_title(item):
    return item['title'].replace(' ', '-')

class ImdbItemPipeline(object):
    # Data issues to deal with
    # movie: {"title": "Jurassic World", "year": "(2015)"}
    # tv: {"title": "Jericho", "year": "(2006\u20132008)"}
    # tv: {"title": "Continuum", "year": "(I) (2012\u20132015)"}
    def process_item(self, item, spider):
        if isinstance(item, ImdbItem):
            if item['title']:
                item['title'] = clean_title(item)
            if item['year']:
                item['year'] = re.sub('^\(.*\)\s|[()]|\u2013([0-9])*','',item['year'])
        return item

class OnDvdItemPipeline(object):
    # Data issues to deal with
    # "year": (2015 film) Action, Sci-Fi
    def process_item(self, item, spider):
        if isinstance(item, OnDvdItem):
            if item['title']:
                item['title'] = clean_title(item)
            if item['year']:
                item['year'] = re.sub('[^0-9]*','',item['year'])
        return item