"""
Authors: Elliot CAMBIER, Owen BRAUX
Created: January 2025
⚠ For personal and educational use only ⚠
"""

from scrapy import signals
import random

class GaultMillauSpiderMiddleware:
    """
    Middleware pour gérer les spiders de Scrapy. Permet d'exécuter
    des actions lorsque le spider est ouvert.
    """
    @classmethod
    def from_crawler(cls, crawler):
        """
        Méthode de classe utilisée par Scrapy pour instancier le middleware.
        
        :param crawler: Instance du crawler Scrapy
        :return: Instance du middleware
        """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):        
        """
        Méthode exécutée lorsqu'un spider est ouvert.
        
        :param spider: Instance du spider Scrapy
        """
        spider.logger.info("Spider ouvert: %s" % spider.name)


class GaultMillauDownloaderMiddleware:
    """
    Middleware pour le gestionnaire de téléchargement Scrapy.
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
    ]

    @classmethod
    def from_crawler(cls, crawler):
        """
        Connecte le signal spider_opened pour initialiser des actions au démarrage
        du spider.
        
        :param crawler: Instance du crawler Scrapy
        :return: Instance du middleware
        """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """
        Assigne un User-Agent aléatoire à la requête pour simuler
        différents navigateurs.
        
        :param request: Requête Scrapy
        :param spider: Instance du spider Scrapy
        """
        request.headers['User-Agent'] = random.choice(self.user_agents)

    def process_response(self, request, response, spider):
        """
        Retourne la réponse sans modification.
        
        :param request: Requête Scrapy
        :param response: Réponse reçue
        :param spider: Instance du spider Scrapy
        :return: Réponse inchangée
        """
        return response

    def process_exception(self, request, exception, spider):
        """
        Méthode exécutée lorsqu' on a une exception pendant le traitement
        
        :param request: Requête Scrapy
        :param exception: Exception levée
        :param spider: Instance du spider Scrapy
        """
        spider.logger.error(f"Exception rencontrée : {exception}")
        pass

    def spider_opened(self, spider):
        """
        Méthode exécutée lorsque le spider est ouvert.
        
        :param spider: Instance du spider Scrapy
        """
        spider.logger.info("Spider ouvert: %s" % spider.name)
