import scrapy
from scrapy.http import Request
from books_crawler.items import BooksCrawlerAdvancedItem

def ProductInfo(response, value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()

class BooksSpider(scrapy.Spider):
    name = 'books_images'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    
    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url,callback=self.parse_book)
        
#        # process next page
#        next_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
#        absolute_next_page_url = response.urljoin(next_url)
#        yield Request(absolute_next_page_url)
    
    def parse_book(self, response):
        # collect data
        title = response.xpath('//h1/text()').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()
        image_url = response.xpath('//img/@src').extract_first().replace('../..','http://books.toscrape.com/')
        
        item = BooksCrawlerAdvancedItem()

        item['title'] = title
        item['price'] = price
        item['image_urls'] = [image_url]

        return item