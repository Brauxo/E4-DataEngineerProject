"""
Authors: Elliot CAMBIER, Owen BRAUX
Created: January 2025
⚠ For personal and educational use only ⚠
"""

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
    photo = scrapy.Field()
