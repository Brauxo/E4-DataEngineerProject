from elasticsearch import Elasticsearch

def get_connection():
    # Crée une connexion à Elasticsearch
    return Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': 'http'}])