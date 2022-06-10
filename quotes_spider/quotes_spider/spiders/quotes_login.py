import scrapy


class QuotesLoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        csrf_token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        yield scrapy.FormRequest(
            'http://quotes.toscrape.com/login', 
            formdata={
                'csrf_token': csrf_token,
                'username': 'blabla',
                'password': 'booboo'
                },
            callback=self.parse_after_login    
            )

    def parse_after_login(self, response):
        if response.xpath('//a[text()="Logout"]'):
            self.log('You are logged in and found the logout button!')