import scrapy

class ArticleItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    address = scrapy.Field()
    chef = scrapy.Field()
    cuisine = scrapy.Field()
    budget = scrapy.Field()
    rating = scrapy.Field()
    category = scrapy.Field()
