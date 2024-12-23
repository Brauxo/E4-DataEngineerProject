"""
Authors: Elliot CAMBIER, Owen BRAUX
Created: January 2025
⚠ For personal and educational use only ⚠
"""
from elasticsearch import Elasticsearch

"""
Module pour gérer la connexion à Elasticsearch.
"""

def get_connection():
    """
    Crée et retourne une connexion à Elasticsearch.

    :return: Instance Elasticsearch connectée au cluster spécifié.
    """
    return Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': 'http'}])