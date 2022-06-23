# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImovirtualItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    local = scrapy.Field()
    location = scrapy.Field()
    county = scrapy.Field()
    area_net = scrapy.Field()
    area_gross = scrapy.Field()
    area_land = scrapy.Field()
    type = scrapy.Field()
    construction_year = scrapy.Field()
    toilets = scrapy.Field()
    energy = scrapy.Field()
    condition = scrapy.Field()
    others = scrapy.Field()
    pool = scrapy.Field()
    alarm = scrapy.Field()
    storage = scrapy.Field()
    central_heating = scrapy.Field()
    air_conditioning = scrapy.Field()
    fireplace = scrapy.Field()
    parking = scrapy.Field()
    garage = scrapy.Field()
    description = scrapy.Field()
