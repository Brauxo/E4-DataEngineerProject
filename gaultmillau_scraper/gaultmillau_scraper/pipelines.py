"""
Authors: Elliot CAMBIER, Owen BRAUX
Created: January 2025
⚠ For personal and educational use only ⚠
"""

import pymongo
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from pymongo.errors import ConnectionFailure
from elasticsearch.exceptions import ConnectionError

class ElasticsearchPipeline:
    """
    Pipeline Scrapy pour insérer les items dans Elasticsearch et MongoDB.
    """
    def open_spider(self, spider):
        """
        Initialisation des connexions à Elasticsearch et MongoDB lorsque le spider est ouvert.
        
        :param spider: Instance du spider Scrapy
        """
        try:
            self.es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': 'http'}])
            self.index_name = "gaultmillau_restaurants"  


            if not self.es.indices.exists(index=self.index_name, request_timeout=30):
                self.es.indices.create(index=self.index_name)
        except ConnectionError as e:
            spider.logger.error(f"Error connecting to Elasticsearch: {e}")
            raise e


        self.items_buffer = []


        try:
            self.mongo_client = pymongo.MongoClient('mongodb://mongodb:27017/')  
            self.mongo_db = self.mongo_client['scrapy_articles']  
            self.mongo_collection = self.mongo_db['articles']  
        except ConnectionFailure as e:
            spider.logger.error(f"Error connecting to MongoDB: {e}")
            raise e

    def close_spider(self, spider):
        """
        Ferme les connexions à Elasticsearch et MongoDB une fois le spider terminé.
        Insère également les derniers items dans Elasticsearch et MongoDB.
        
        :param spider: Instance du spider Scrapy
        """       
        if self.items_buffer:
            self._bulk_insert_items()

        
        self.es.close()
        self.mongo_client.close()

    def process_item(self, item, spider):
        """
        Traite chaque item extrait par le spider en :
        - Préparant l'item pour Elasticsearch
        - L'insèrant dans MongoDB
        - Gèrant l'insertion en masse dans Elasticsearch pour améliorer les performances
        
        :param item: Item extrait par le spider
        :param spider: Instance du spider Scrapy
        :return: L'item traité
        """     
        doc = {
            "_index": self.index_name,
            "_source": dict(item)
        }
        self.items_buffer.append(doc)

        
        try:
            self.mongo_collection.insert_one(dict(item))
        except Exception as e:
            spider.logger.error(f"Failed to insert item into MongoDB: {e}")

        
        if len(self.items_buffer) >= 100:
            self._bulk_insert_items()

        return item

    def _bulk_insert_items(self):
        """
        Effectue une insertion en masse dans Elasticsearch pour améliorer les performances puis vide le buffer.
        """  
        try:
            bulk(self.es, self.items_buffer)
        except Exception as e:
            print(f"Failed to perform bulk insert into Elasticsearch: {e}")
        finally:
            self.items_buffer = []
