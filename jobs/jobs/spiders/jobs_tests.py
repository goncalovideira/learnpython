import scrapy

from jobs.items import JobsItem

# https://docs.scrapy.org/en/latest/intro/tutorial.html

# --- SPIDER ---

class LinkedIn (scrapy.Spider): 
    name = 'galp'

    def start_requests(self):
        urls = ['https://jobs.galp.com/go/Oportunidades/1335501/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        item = JobsItem()
        jobs = response.xpath("//td/span[contains(@class, 'jobTitle hidden-phone')]")
        for job in jobs:
            item['jobTitle'] = job.css('a::text').get()
            item['jobURL'] = job.css('::attr(href)').get()
            yield item
