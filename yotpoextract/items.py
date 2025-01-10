# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YotpoextractItem(scrapy.Item):
    reviews_id = scrapy.Field()
    review_content =scrapy.Field()
    review_title = scrapy.Field()
    review_date = scrapy.Field()
    review_rating = scrapy.Field()
    


