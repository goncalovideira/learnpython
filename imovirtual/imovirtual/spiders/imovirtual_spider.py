import scrapy
from scrapy.http import Request
import re

class ImovirtualSpiderSpider(scrapy.Spider):
    name = 'imovirtual_spider'
    allowed_domains = ['imovirtual.com']
    start_urls = ['https://www.imovirtual.com/arrendar/moradia/lisboa/?search%5Bregion_id%5D=11&search%5Bsubregion_id%5D=153']

    def parse(self, response):
        # get page title in h1
        page_title = response.xpath('//h1/strong/text()').extract_first()
        
        # get al offers in page and iterate over offers
        offers = response.xpath('//article')
        for offer in offers: 
            offer_link = offer.xpath('.//@data-url').extract_first()
            offer_title = offer.xpath('.//*[@class="offer-item-title"]/text()').extract_first()
            offer_price = offer.xpath('.//*[@class="offer-item-price"]/text()').extract_first().strip()
        
            yield Request(offer_link, callback=self.parse_offer)
        
        # find next page link and follow link if exists
        next_page = response.xpath('//*[@class="pager-next"]/a/@href').extract_first()
        if next_page:
            yield Request(next_page, callback=self.parse)
        
    def parse_offer(self, response):
        title = response.xpath('//h1/text()').extract_first()
        price = response.xpath('//*[@aria-label="Preço"]/text()').extract_first().replace('€','').replace(' ','')
        local = response.xpath('//*[@aria-label="Endereço"]/text()').extract_first()
        parish = local.split(',')[0].strip()
        county = local.split(',')[1].strip()
        area_net = response.xpath('//*[contains(@aria-label,"Área útil")]/div[2]/@title').extract_first().split(' ')[0]
        area_gross = response.xpath('//*[contains(@aria-label,"Área bruta")]/div[2]/@title').extract_first()
        # area_gross = area_gross.replace('m','').replace(' ','')
        # area_gross = re.sub(u'\u00B2','',area_gross)
        area_land = response.xpath('//*[contains(@aria-label,"Área de terreno")]/div[2]/@title').extract_first()
        # area_land = area_land.replace('m','').replace(' ','')
        # area_land = re.sub(u'\u00B2','',area_land)
        type = response.xpath('//*[contains(@aria-label,"Tipologia")]/div[2]/@title').extract_first()
        construction_year = response.xpath('//*[contains(@aria-label,"Ano de construção")]/div[2]/@title').extract_first()
        toilets = response.xpath('//*[contains(@aria-label,"Casas de Banho")]/div[2]/@title').extract_first()
        energy = response.xpath('//*[contains(@aria-label,"Certificado Energético")]/div[2]/@title').extract_first()
        condition = response.xpath('//*[contains(@aria-label,"Condição")]/div[2]/@title').extract_first()
        others = response.xpath('//*[@data-cy="ad.ad-features.uncategorized-list"]/li/text()').extract()
        pool = 'Piscina' in others
        alarm = 'Alarme' in others
        storage = 'Arrecadação' in others
        central_heating = 'Aquecimento Central' in others
        air_conditioning = 'Ar Condicionado' in others
        fireplace = 'Lareira' in others
        parking = 'Estacionamento' in others
        for other in others:
            if 'Garagem' in other:
                garage = True
        description = response.xpath('//*[@data-cy="adPageAdDescription"]/text()').extract()

        yield {
            'title': title,
            'price': price,
            'parish': parish,
            'county': county
        }
        