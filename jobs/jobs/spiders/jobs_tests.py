import scrapy

# https://docs.scrapy.org/en/latest/intro/tutorial.html

# --- SPIDER ---

class LinkedIn (scrapy.Spider): 
    name = 'sonae'

    def start_requests(self):
        urls = ['https://www.sonae.pt/pt/pessoas/oportunidades-de-carreira/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
        yield response.body
