import scrapy
from ..items import ArticleItem

class GaultMillauSpider(scrapy.Spider):
    name = "gaultmillau"
    allowed_domains = ["fr.gaultmillau.com"]

    # URL de base pour la pagination
    start_urls = ["https://fr.gaultmillau.com/fr/search/restaurant"]

    # Limite de pages pour le test
    page_limit = 2  # Changez ce nombre pour limiter le nombre de pages scrappées
    current_page = 0  # Compteur de pages scrappées

    def parse(self, response):
        # Vérifier si la limite de pages est atteinte
        if self.current_page >= self.page_limit:
            self.logger.info("Limite de pages atteinte, arrêt du crawling.")
            return

        # Sélectionner chaque bloc de restaurant
        restaurants = response.css('.BaseCard.RestaurantCard')

        # Si aucune carte de restaurant n'est trouvée, arrêter le crawling
        if not restaurants:
            self.logger.info("Aucun restaurant trouvé, fin de la pagination.")
            return

        for restaurant in restaurants:
            item = ArticleItem()

            # Nom du restaurant
            name = restaurant.css('h3::text').get()
            item['name'] = name.strip() if name else None

            # URL du restaurant
            url = restaurant.css('a.stretched-link::attr(href)').get()
            item['url'] = response.urljoin(url) if url else None

            # Adresse
            address = restaurant.css('.column2.fw-bold::text').get()
            item['address'] = address.strip() if address else None

            # Chef
            chef = restaurant.xpath(
                './/span[contains(text(), "Chef")]/following-sibling::span[@class="column2"]/text()').get()
            item['chef'] = chef.strip() if chef else None

            # Cuisine
            cuisine = restaurant.css('.column2.roundedText.positonedManual::text').get()
            item['cuisine'] = cuisine.strip() if cuisine else None

            # Budget
            budget = restaurant.xpath(
                './/span[contains(text(), "Budget")]/following-sibling::span[@class="column2"]/text()').get()
            item['budget'] = budget.strip() if budget else None

            # Note (Rating) - Cas spécial pour "Membre de l'Académie Gault&Millau"
            rating = restaurant.css('.ResumeSelection .row0 b::text').get()
            if not rating:
                category = restaurant.css('.ResumeSelection .row1::text').get()
                if category and "Membre de l'Académie Gault&Millau" in category:
                    item['rating'] = "20"
                else:
                    item['rating'] = None
            else:
                item['rating'] = rating.strip()

            # Catégorie
            category = restaurant.css('.ResumeSelection .row1::text').get()
            item['category'] = category.strip() if category else None

            yield item

        # Incrémenter le compteur de pages
        self.current_page += 1

        # Pagination : détecter si on est sur la première page, puis avancer par incréments de 15
        if "restaurant/" in response.url:
            current_page = int(response.url.split('/')[-1].split('#')[0])
            next_page = current_page + 15
        else:
            next_page = 15  # Démarrer à la première page avec offset de 15

        next_url = f"https://fr.gaultmillau.com/fr/search/restaurant/{next_page}#search"

        # Passer à la page suivante
        yield scrapy.Request(next_url, callback=self.parse)
