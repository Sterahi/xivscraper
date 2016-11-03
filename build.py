import scrapy

class xivSpider(scrapy.Spider):
    name = 'xiv_spider'
    start_urls = ['http://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=1']

    def parse(self, response):
        ITEM_SELECTOR = 'tr'  # Getting class to pull base info from
        for xiv in response.css(ITEM_SELECTOR):
            NAME_SELECTOR = 'td div .db-table__txt--detail_link ::text'  # CSS identifier for the set name
            LINK_SELECTOR = 'td div .db-table__txt--detail_link ::attr(href)'
            yield {
                'name': xiv.css(NAME_SELECTOR).extract_first(),
                'link': xiv.css(LINK_SELECTOR).extract_first(),
            }
        NEXT_PAGE_SELECTOR ='.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
