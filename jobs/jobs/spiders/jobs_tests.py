import scrapy

# https://docs.scrapy.org/en/latest/intro/tutorial.html

# --- SPIDER ---

class LinkedIn (scrapy.Spider): 
    name = 'galp'

    def start_requests(self):
        urls = ['https://jobs.galp.com/go/Oportunidades/1335501/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
