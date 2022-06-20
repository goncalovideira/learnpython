scrapy shell "https://www.hkexnews.hk/sdw/search/searchsdw.aspx"

from scrapy.http import FormRequest

data = {'__EVENTTARGET': 'btnSearch',
        '__VIEWSTATE': response.xpath('//*[@name="__VIEWSTATE"]/@value').extract_first(),
        '__VIEWSTATEGENERATOR': response.xpath('//*[@name="__VIEWSTATEGENERATOR"]/@value').extract_first(),
        'today': '20191030',
        'sortBy': 'shareholding',
        'sortDirection': 'desc',
        'txtShareholdingDate': '2019/10/29',
        'txtStockCode': '00001'}

page = FormRequest('https://www.hkexnews.hk/sdw/search/searchsdw.aspx',
                   formdata=data)

fetch(page)
