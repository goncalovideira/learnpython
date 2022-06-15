import scrapy
from scrapy.http import Request


class ClassspiderSpider(scrapy.Spider):
    name = 'classspider'
    allowed_domains = ['classcentral.com']
    start_urls = ['http://www.classcentral.com/subjects']

    def __init__(self, subject=None):
        self.subject = subject

    def parse(self, response):
        if self.subject:
            print(self.subject)
                    
            # fetch subject urls
            subj_url = response.xpath('//a[contains(@title,"' + self.subject + '")]/@href').extract_first()
            abs_subj_url = response.urljoin(subj_url)

            yield Request(abs_subj_url, callback=self.parse_subject)
        
        else:
            self.log('Scraping all subjects.')

            # fetch ALL subject urls and loop through them
            subj_urls = response.xpath('//h3[@class="row vert-align-middle"]/a[@class="border-box align-middle padding-right-xsmall"]/@href').extract()
            for subject in subj_urls:
                abs_subj_url = response.urljoin(subject)
                yield Request(abs_subj_url, callback=self.parse_subject)
    
    def parse_subject(self, response): 
        subject = response.xpath('//h1/text()').extract_first()
        courses = response.xpath('//*[@itemtype="http://schema.org/Event"]')
        for course in courses: 
            name = course.xpath('.//*[@itemprop="name"]/text()').extract_first()
            url = course.xpath('.//a[@class="color-charcoal course-name"]/@href').extract_first()
            abs_url = response.urljoin(url)

            yield {
                'Subject': subject,
                'CourseName': name,
                'URL': abs_url
            }

        # check if there is a next page and follow through
        next_page = response.xpath('//link[@rel="next"]/@href').extract_first()
        if next_page:
            abs_next_page = response.urljoin(next_page)
            yield Request(abs_next_page, callback=self.parse_subject)


