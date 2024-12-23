"""
Authors: Elliot CAMBIER, Owen BRAUX
Created: January 2025
⚠ For personal and educational use only ⚠
"""

import scrapy
from ..items import ArticleItem

class GaultMillauSpider(scrapy.Spider):
    """
    Spider Scrapy pour scraper les informations des restaurants depuis le site Gault&Millau.
    """
    name = "gaultmillau"
    allowed_domains = ["fr.gaultmillau.com"]

    # URL 
    start_urls = ["https://fr.gaultmillau.com/fr/search/restaurant"]

    def parse(self, response):
        """
        Fonction principale de parsing :
        - Scrape les informations des restaurants sur chaque page. (nom,url du restau,adresse,chef,type de cuisine,budget,la note, la categorie et la photo)
        - Gère la pagination.
        
        :param response: Réponse HTML renvoyée par Scrapy pour la page actuelle.
        """
        restaurants = response.css('.BaseCard.RestaurantCard')


        if not restaurants:
            self.logger.info("Aucun restaurant trouvé, fin de la pagination.")
            return

        for restaurant in restaurants:
            item = ArticleItem()


            name = restaurant.css('h3::text').get()
            item['name'] = name.strip() if name else None


            url = restaurant.css('a.stretched-link::attr(href)').get()
            item['url'] = response.urljoin(url) if url else None


            address = restaurant.css('.column2.fw-bold::text').get()
            item['address'] = address.strip() if address else None


            chef = restaurant.xpath(
                './/span[contains(text(), "Chef")]/following-sibling::span[@class="column2"]/text()').get()
            item['chef'] = chef.strip() if chef else None


            cuisine = restaurant.css('.column2.roundedText.positonedManual::text').get()
            if cuisine:
                cuisines = [c.strip() for c in cuisine.split('|') if
                            c.strip()]
                item['cuisine'] = cuisines
            else:
                item['cuisine'] = None


            budget = restaurant.xpath(
                './/span[contains(text(), "Budget")]/following-sibling::span[@class="column2"]/text()').get()
            item['budget'] = budget.strip() if budget else None

            # Note (Rating) - Cas spécial pour "Membre de l'Académie Gault&Millau"
            rating = restaurant.css('.ResumeSelection .row0 b::text').get()
            if not rating:
                category = restaurant.css('.ResumeSelection .row1::text').get()
                if category and "Membre de l'Académie Gault&Millau" in category:
                    item['rating'] = 20.0   
                else:
                    item['rating'] = None
            else:
                try:
                    item['rating'] = float(rating.strip())
                except ValueError:
                    item['rating'] = None


            category = restaurant.css('.ResumeSelection .row1::text').get()
            item['category'] = category.strip() if category else None


            photo = restaurant.css('picture img::attr(src)').get()
            item['photo'] = photo.strip() if photo else None

            yield item

        # Pagination : détecter si on est sur la première page, puis avancer par incréments de 15
        if "restaurant/" in response.url:
            current_page = int(response.url.split('/')[-1].split('#')[0])
            next_page = current_page + 15
        else:
            next_page = 15  # Démarrer à la première page avec offset de 15

        next_url = f"https://fr.gaultmillau.com/fr/search/restaurant/{next_page}#search"

        # Passe à la page suivante.
        yield scrapy.Request(next_url, callback=self.parse)
