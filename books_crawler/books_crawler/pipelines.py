# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os

class BooksCrawlerRenamePipeline:
    def process_item(self, item, spider):
        os.chdir('C:/Users/gonca/OneDrive - BYZAPP LABS/DeveloperPlan/learnpython/books_crawler/Images')
        if item['images'][0]['path']:
            new_name = item['title'] + '.jpg'
            new_name = new_name.replace(':','')
            new_path = 'full/' + new_name

            os.rename(item['images'][0]['path'], new_path)
