# Utiliser une image de base Python
FROM python:3.9-slim

# Installer les dépendances requises
RUN pip install scrapy elasticsearch
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copier les fichiers du dossier local vers le conteneur
COPY . /app
WORKDIR /app

# Commande par défaut pour vérifier les données et exécuter Scrapy
CMD ["sh", "-c", " if curl -s http://elasticsearch:9200/gaultmillau_restaurants | grep 'index_not_found_exception';then scrapy crawl gaultmillau;else echo 'Data already present in Elasticsearch, skipping scraping';fi"]
