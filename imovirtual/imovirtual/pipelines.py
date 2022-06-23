# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class ImovirtualCleanDataPipeline:
    def process_item(self, item, spider):
        if item['price']:
            item['price'] = item['price'].replace('€','').replace(' ','')
        
        if item['location']:
            item['location'] = item['location'].strip()

        if item['county']:
            item['county'] = item['county'].strip()
        
        if item['area_net']:
            item['area_net'] = item['area_net'].split(' ')[0]
        
        if item['area_gross']:
            item['area_gross'] = item['area_gross'].replace('m','').replace(' ','')
            item['area_gross'] = re.sub(u'\u00B2','',item['area_gross'])
        
        if item['area_land']:
            item['area_land'] = item['area_land'].replace('m','').replace(' ','')
            item['area_land'] = re.sub(u'\u00B2','',item['area_land'])

        if item['description']:
                item['description'] = ' '.join(item['description'])
                item['description'] = re.sub(r'\r','',item['description'])
                item['description'] = re.sub(r'\n','',item['description'])
                item['description'] = re.sub(u'\xa0',' ',item['description'])
                item['description'] = item['description'].strip()
        return item
