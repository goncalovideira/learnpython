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

            yield {
                'Date': date_time,
                'Title': title,
                'Link': link
            }

