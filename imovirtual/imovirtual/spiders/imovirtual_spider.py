import scrapy


class ImovirtualSpiderSpider(scrapy.Spider):
    name = 'imovirtual_spider'
    allowed_domains = ['imovirtual.com']
    start_urls = ['https://www.imovirtual.com/arrendar/moradia/belem-lisboa/']

    def parse(self, response):
        # get page title in h1
        page_title = response.xpath('//h1/strong/text()').extract_first()
        
        # get al offers in page and iterate over offers
        offers = response.xpath('//article')
        for offer in offers: 
            offer_link = offer.xpath('.//@data-url').extract_first()
            offer_title = offer.xpath('.//*[@class="offer-item-title"]/text()').extract_first()
            offer_price = offer.xpath('.//*[@class="offer-item-price"]/text()').extract_first().strip()
        
            yield {
                'page title': page_title,
                'offer link': offer_link,
                'offer title': offer_title,
                'offer price': offer_price
            }

