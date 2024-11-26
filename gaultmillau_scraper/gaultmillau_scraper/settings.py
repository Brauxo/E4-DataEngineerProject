BOT_NAME = "gaultmillau_scraper"

SPIDER_MODULES = ["gaultmillau_scraper.spiders"]
NEWSPIDER_MODULE = "gaultmillau_scraper.spiders"

# Désactiver l'obéissance au fichier robots.txt
ROBOTSTXT_OBEY = False


# Activer l'AutoThrottle pour ajuster automatiquement le délai en fonction de la charge
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 5

# Définir un User-Agent pour réduire le risque de blocage
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'

DOWNLOADER_MIDDLEWARES = {
    'gaultmillau_scraper.middlewares.GaultMillauDownloaderMiddleware': 543,
}
ITEM_PIPELINES = {
    'gaultmillau_scraper.pipelines.ElasticsearchPipeline': 300,
}
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Enable your custom pipelines for both Elasticsearch and MongoDB
ITEM_PIPELINES = {
    'your_project_name.pipelines.ElasticsearchPipeline': 1,
}

# Add MongoDB specific settings if necessary
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'scrapy_articles'

