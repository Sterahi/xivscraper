import scrapy
import collections

linkqueue = collections.deque()

class weaponSpider(scrapy.Spider):
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
            linkqueue.append(xiv.css(LINK_SELECTOR).extract_first())
        NEXT_PAGE_SELECTOR ='.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
        elif len(linkqueue) >=1:
            for link in list(linkqueue):
                next_page = "http://na.finalfantasyxiv.com/" + str(linkqueue[0])
                linkqueue.popleft()
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parseStats
                )
            next_page = "http://na.finalfantasyxiv.com/lodestone/playguide/db/item/?category2=3"
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

    def parseStats(self, response):
        TABLE_SELECT = 'ul.db-view__basic_bonus'
        NAME_SELECT = 'normalize-space(//div/div/div/div/div/div/h2/text())'
        STAT1_SELECT = '//div/div/div/div/div/div/div/div/ul/li[1]/span/text()'
        VALUE1_SELECT = '//div/div/div/div/div/div/ul/li[1]/text()'
        STAT2_SELECT = '//div/div/div/div/div/div/div/div/ul/li[2]/span/text()'
        VALUE2_SELECT = '//div/div/div/div/div/div/ul/li[2]/text()'
        STAT3_SELECT = '//div/div/div/div/div/div/div/div/ul/li[3]/span/text()'
        VALUE3_SELECT = '//div/div/div/div/div/div/ul/li[3]/text()'
        STAT4_SELECT = '//div/div/div/div/div/div/div/div/ul/li[4]/span/text()'
        VALUE4_SELECT = '//div/div/div/div/div/div/ul/li[4]/text()'
        for stat in response.css(TABLE_SELECT):
            yield {
                'name': stat.xpath(NAME_SELECT).extract(),
                'stat1': stat.xpath(STAT1_SELECT).extract_first(),
                'stat1#':stat.xpath(VALUE1_SELECT).extract_first(),
                'stat2': stat.xpath(STAT2_SELECT).extract_first(),
                'stat2#':stat.xpath(VALUE2_SELECT).extract_first(),
                'stat3': stat.xpath(STAT3_SELECT).extract_first(),
                'stat3#':stat.xpath(VALUE3_SELECT).extract_first(),
                'stat4': stat.xpath(STAT4_SELECT).extract_first(),
                'stat4#':stat.xpath(VALUE4_SELECT).extract_first(),
            }
