import scrapy


class CrunchbaseSpider(scrapy.Spider):
    name = 'crunchbase'
    allowed_domains = ['crunchbase.com']
    start_urls = ['https://www.crunchbase.com/organization/spell']

    def parse(self, response):
        pass
