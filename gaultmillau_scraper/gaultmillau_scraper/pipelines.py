from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class ElasticsearchPipeline:

    def open_spider(self, spider):
        # Connexion à Elasticsearch
        self.es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': 'http'}])
        self.index_name = "gaultmillau_restaurants"  # Nom de l'index dans Elasticsearch

        # Créer l'index s'il n'existe pas déjà
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name)

        # Liste temporaire pour les items à insérer en bulk
        self.items_buffer = []

    def close_spider(self, spider):
        # Insérer les items restants
        if self.items_buffer:
            self._bulk_insert_items()
        self.es.close()

    def process_item(self, item, spider):
        # Préparer l'item pour l'insertion dans Elasticsearch
        doc = {
            "_index": self.index_name,
            "_source": dict(item)
        }
        self.items_buffer.append(doc)

        # Insérer en bulk tous les 100 items pour une meilleure performance
        if len(self.items_buffer) >= 100:
            self._bulk_insert_items()

        return item

    def _bulk_insert_items(self):
        bulk(self.es, self.items_buffer)
        self.items_buffer = []
