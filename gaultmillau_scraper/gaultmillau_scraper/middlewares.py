from scrapy import signals
import random

class GaultMillauSpiderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        # Cette méthode est utilisée par Scrapy pour créer les spiders
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.logger.info("Spider ouvert: %s" % spider.name)


class GaultMillauDownloaderMiddleware:

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
    ]

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Sélectionne un User-Agent aléatoire pour chaque requête
        request.headers['User-Agent'] = random.choice(self.user_agents)

    def process_response(self, request, response, spider):
        # Retourne la réponse sans modification
        return response

    def process_exception(self, request, exception, spider):
        # Log l'exception pour une éventuelle analyse
        spider.logger.error(f"Exception rencontrée : {exception}")
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider ouvert: %s" % spider.name)
