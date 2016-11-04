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
        NEXT_PAGE_SELECTOR = LINK_SELECTOR
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
            "http://na.finalfantasyxiv.com/" + next_page,
                callback=self.parseStats
            )

    def parseStats(self, response):
        TABLE_SELECT = 'ul.db-view__basic_bonus'
        STAT_SELECT = 'li li ::text'
        VALUE_SELECT = 'li ::text'
        for stat in response.css(TABLE_SELECT):
            yield {
                'stat1': stat.css(STAT_SELECT).extract_first(),
                'stat1#':stat.css(VALUE_SELECT).extract_first(),
            }
