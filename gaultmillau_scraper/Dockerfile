# Utiliser une image de base Python
FROM python:3.9-slim

# Installer les dépendances requises
RUN pip install scrapy elasticsearch

# Copier les fichiers du dossier local vers le conteneur
COPY . /app
WORKDIR /app

# Commande par défaut pour exécuter Scrapy (ajustez le nom du spider)
CMD ["scrapy", "crawl", "gaultmillau"]
