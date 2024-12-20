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

    def open_spider(self, spider):
        # Connect to Elasticsearch
        try:
            self.es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': 'http'}])
            self.index_name = "gaultmillau_restaurants"  # Elasticsearch index name

            # Create the index if it doesn't exist
            if not self.es.indices.exists(index=self.index_name, request_timeout=30):
                self.es.indices.create(index=self.index_name)
        except ConnectionError as e:
            spider.logger.error(f"Error connecting to Elasticsearch: {e}")
            raise e

        # Temporary list for bulk inserting items into Elasticsearch
        self.items_buffer = []

        # Connect to MongoDB
        try:
            self.mongo_client = pymongo.MongoClient('mongodb://mongodb:27017/')  # Docker MongoDB hostname
            self.mongo_db = self.mongo_client['scrapy_articles']  # MongoDB database name
            self.mongo_collection = self.mongo_db['articles']  # MongoDB collection name
        except ConnectionFailure as e:
            spider.logger.error(f"Error connecting to MongoDB: {e}")
            raise e

    def close_spider(self, spider):
        # Insert the remaining items into Elasticsearch and MongoDB
        if self.items_buffer:
            self._bulk_insert_items()

        # Close MongoDB and Elasticsearch connections
        self.es.close()
        self.mongo_client.close()

    def process_item(self, item, spider):
        # Prepare the item for insertion into Elasticsearch
        doc = {
            "_index": self.index_name,
            "_source": dict(item)
        }
        self.items_buffer.append(doc)

        # Insert the item into MongoDB
        try:
            self.mongo_collection.insert_one(dict(item))
        except Exception as e:
            spider.logger.error(f"Failed to insert item into MongoDB: {e}")

        # Insert in bulk every 100 items for better performance (Elasticsearch only)
        if len(self.items_buffer) >= 100:
            self._bulk_insert_items()

        return item

    def _bulk_insert_items(self):
        # Perform the bulk insert into Elasticsearch
        try:
            bulk(self.es, self.items_buffer)
        except Exception as e:
            print(f"Failed to perform bulk insert into Elasticsearch: {e}")
        finally:
            self.items_buffer = []
