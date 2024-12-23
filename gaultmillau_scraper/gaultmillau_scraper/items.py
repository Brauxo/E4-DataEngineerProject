"""
Authors: Elliot CAMBIER, Owen BRAUX
Created: January 2025
⚠ For personal and educational use only ⚠
"""

import scrapy

class ArticleItem(scrapy.Item):
    """
    Définition des items pour Scrapy.
    Représente les données extraites pour un article/restaurant sur le site Gault&Millau.
    Chaque champ correspond à une donnée spécifique à collecter.
    """
    name = scrapy.Field()
    url = scrapy.Field()
    address = scrapy.Field()
    chef = scrapy.Field()
    cuisine = scrapy.Field()
    budget = scrapy.Field()
    rating = scrapy.Field()
    category = scrapy.Field()
    photo = scrapy.Field()
