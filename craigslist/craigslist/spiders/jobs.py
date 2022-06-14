from subprocess import call
from numpy import absolute
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ['http://newyork.craigslist.org/search/egr']

    def parse(self, response):
        # get listing rows
        listings = response.xpath('//*[@class="result-row"]')

        for listing in listings:
            date_time = listing.xpath('.//*[@class="result-date"]/@datetime').extract_first()
            title = listing.xpath('.//a[@class="result-title hdrlnk"]/text()').extract_first()
            link = listing.xpath('.//a[@class="result-title hdrlnk"]/@href').extract_first()

            yield scrapy.Request(
                link, 
                callback=self.parse_listing,
                meta={
                    'date': date_time,
                    'title': title,
                    'link': link
                }
            )
            next_page_url = response.xpath('//a[@class="button next"]/@href').extract_first()
            absolute_next_page_url = response.urljoin(next_page_url)
            if next_page_url:
                yield scrapy.Request(absolute_next_page_url, callback=self.parse)

    def parse_listing(self, response):
        date = response.meta['date']
        link = response.meta['link']
        title = response.meta['title']

        salary = response.xpath('//*[@class="attrgroup"]/span[contains(text(),"compensation")]/b/text()').extract_first()
        employment_type = response.xpath('//*[@class="attrgroup"]/span[contains(text(),"employment")]/b/text()').extract_first()

        thumbs = response.xpath('//*[@id="thumbs"]//img/@src').extract()
        if thumbs:
            images = [image.replace('50x50c', '600x450') for image in thumbs]
        else:
            images = []
        
        description = response.xpath('//*[@id="postingbody"]/text()').extract()

        yield {
            'date': date,
            'link': link,
            'title': title,
            'salary': salary,
            'type': employment_type,
            'images': images,
            'description': description
        }