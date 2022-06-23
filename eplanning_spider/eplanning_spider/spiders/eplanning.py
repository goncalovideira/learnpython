from urllib.request import Request
import scrapy
from scrapy.http import Request, FormRequest


class EplanningSpider(scrapy.Spider):
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = [
        'http://www.eplanning.ie/'
        ]

    def parse(self, response):
        urls = response.xpath('//a/@href').extract()
        for url in urls:
            if '#' == url:
                pass
            else:
                yield Request(url, callback=self.parse_application)
    
    def parse_application(self, response):
        app_url = response.xpath('//*[@class="glyphicon glyphicon-inbox btn-lg"]/following-sibling::a/@href').extract_first()
        yield Request(response.urljoin(app_url), callback=self.parse_form)

    def parse_form(self, response):
        yield FormRequest.from_response(
            response,
            formdata={'RdoTimeLimit': '42'},
            dont_filter=True,
            formxpath='(//form)[2]',
            callback=self.parse_pages
            )
    
    def parse_pages(self, response):
        links = response.xpath('//td/a/@href').extract()
        for link in links: 
            yield Request(response.urljoin(link), callback=self.parse_items)

        next_url = response.xpath('//*[@rel="next"]/@href').extract_first()
        if next_url:
            yield Request(response.urljoin(next_url), callback=self.parse_pages)
    
    def parse_items(self, response):
        agent_btn = response.xpath('//*[@value="Agents" and @style="display: inline;  visibility: visible;"]')
        if agent_btn:
            name = response.xpath('//*[@title="Agent Details"]/table/tr[th="Name :"]/td/text()').extract_first()

            address_first = response.xpath('//*[@title="Agent Details"]/table/tr[th="Address :"]/td/text()').extract()
            address_second = response.xpath('//*[@title="Agent Details"]/table/tr[th="Address :"]/following-sibling::tr/td/text()').extract()[:3]
            address = address_first + address_second

            phone = response.xpath('//*[@title="Agent Details"]/table/tr[th="Phone :"]/td/text()').extract_first()
            fax = response.xpath('//*[@title="Agent Details"]/table/tr[th="Fax :"]/td/text()').extract_first()
            email = response.xpath('//*[@title="Agent Details"]/table/tr[th="e-mail :"]/td/a/text()').extract_first()

            url = response.url

            yield {
                'Name': name,
                'Address': address,
                'Phone': phone,
                'Fax': fax,
                'Email': email,
                'URL': url
            }

        else:
            self.logger.info('Agents button not found on page. Passing invalid url!')