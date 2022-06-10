import scrapy
from scrapy.http import Request

def ProductInfo(response, value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    
    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url,callback=self.parse_book)
        next_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_url)
        yield Request(absolute_next_page_url)
    
    def parse_book(self, response):
        title = response.xpath('//h1/text()').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()
        image_url = response.xpath('//img/@src').extract_first().replace('../../','https://books.toscrape.com/')
        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first().replace('star-rating ', '')
        description = response.xpath('//*[@class="product_page"]/p/text()').extract_first()

        # product information
        upc = ProductInfo(response, 'UPC')
        type = ProductInfo(response, 'Product Type')
        price_without_tax = ProductInfo(response, 'Price (excl. tax)')
        price_with_tax = ProductInfo(response, 'Price (incl. tax)')
        tax = ProductInfo(response, 'Tax')
        availability = ProductInfo(response, 'Availability')
        number_reviews = ProductInfo(response, 'Number of reviews')
        
        yield {
            'title': title,
            'price': price,
            'image_url': image_url,
            'rating': rating,
            'description': description,
            'upc': upc,
            'type': type,
            'price_without_tax': price_without_tax,
            'price_with_tax': price_with_tax,
            'tax': tax,
            'availability': availability,
            'number_reviews': number_reviews

        }

