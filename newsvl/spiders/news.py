import scrapy
from newsvl.items import NewsItem


class NewsSpider(scrapy.Spider):
    name = 'newsvl'
    start_urls = ['https://www.newsvl.ru']
    page_counter = 12
    counter = 1
    iter = 0
    links = []
    str = start_urls[0]

    def parse(self, response, **kwargs):
        if response.css(".story__content"):
            items = NewsItem()
            datetime = response.css(".story .story__info .story__info-date ::text").extract_first()
            title = response.css(".story .story__title ::text").extract_first()
            story = response.css(".story__text ::text").extract()
            url = response.url
            items['url'] = url
            items['story'] = story
            items['title'] = title
            items['datetime'] = datetime
            yield items

        elif self.counter <= self.page_counter:
                self.links += response.css(".story-list__item-title a::attr(href)").extract()
                self.counter += 1
                self.str = self.start_urls[0] + '/?page=' + str(self.counter)
                yield scrapy.Request(self.str, callback=self.parse)
        else:
            for link in self.links:
                yield scrapy.Request(self.start_urls[0] + link, callback=self.parse)
