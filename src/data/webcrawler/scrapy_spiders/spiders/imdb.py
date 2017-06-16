import scrapy
from scrapy.exceptions import CloseSpider
from scrapy_spiders.items import ImdbItem

class SpiderIMDB(scrapy.Spider):
    name='imdb_com'

    start_urls = [
        'http://www.imdb.com/search/title?genres=sci_fi&title_type=feature&page=1&sort=boxoffice_gross_us,desc&ref_=adv_prv',
        'http://www.imdb.com/search/title?genres=sci_fi&title_type=tv_series&sort=num_votes,desc&page=1&ref_=adv_prv'
    ]

    def parse(self, response):

        for titles in response.css('div.lister-item-content'):
            item = ImdbItem()
            item['title'] = titles.css('h3.lister-item-header a::text').extract_first()
            item['year'] = titles.css('span.lister-item-year::text').extract_first()
            yield item

        # Stop parsing if page limit is reached
        self.enforce_page_limit(response)

        # follow pagination links
        for href in response.css('div.desc a::attr(href)'):
            yield response.follow(href, self.parse)

    def enforce_page_limit(self, response):
        if '&page=1&' in str(response.body):
            raise CloseSpider('reached requested page limit')