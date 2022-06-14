import scrapy


class RemaxSpider(scrapy.Spider):
    name = 'remax'
    allowed_domains = ['remax.pt']
    start_urls = ['https://www.remax.pt/']

    def parse(self, response):
        yield response.xpath('//h1').extract_first()
