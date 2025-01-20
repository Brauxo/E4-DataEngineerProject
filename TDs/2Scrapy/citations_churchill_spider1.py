import scrapy

class ChurchillQuotesSpider(scrapy.Spider):
    name = "churchill_quotes"
    start_urls = ["http://evene.lefigaro.fr/citations/winston-churchill"]

    def parse(self, response):
        for cit in response.xpath('//div[@class="figsco__quote__text"]'):
            text_value = cit.xpath('a/text()').extract_first()
            author = "Winston Churchill"  

            yield {
                'text': text_value,
                'author': author
            }
        next_page = response.xpath('//a[@class="pagination__next"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)