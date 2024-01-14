import scrapy


class MagentoSpider(scrapy.Spider):
    name = "Magento"
    start_urls = ["https://sanitairkamer.nl/"]


    def parse(self, response):

        for i in response.css('.navigation__third-wrapper a.navigation__secondary-link::attr(href)').getall():
            i = response.urljoin(i)
            yield scrapy.Request(i, callback=self.parse_link)

    def parse_link(self, response):

        for item in response.css('.product-list__item'):
            link = item.css(
                'div.product-card__name-desc > a::attr(href)').get()
            link = response.urljoin(link)

            yield scrapy.Request(link, callback=self.parse_city)
            
                      
        # crawling next page
        next_link = response.css(
            'div.toolbar.toolbar-products.toolbar--bottom > div.toolbar__pager > div > ul > li.item.pages-item-next > a::attr(href)').get()
        
        if next_link:
            next_link = response.urljoin(next_link)
            yield scrapy.Request(next_link, callback=self.parse_link)

    def parse_city(self, response):
        long = response.css('div #description p::text').getall()
        if long == None:
            long = response.css('#description > div > div.value::text').getall()

        yield {
            'url': response.url,
            'short-description': response.css('div.product-page__header.product-column__right > div > h1::text').get(),
            'price': response.css('.product-page__price .price::text').get().encode('ascii', 'ignore').decode('utf-8').strip(),
            'long-description': long

        }

        