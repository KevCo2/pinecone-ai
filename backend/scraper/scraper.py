import scrapy

class ProductSpider(scrapy.Spider):
    name = 'product_spider'
    start_urls = [
        # Add e-commerce URLs here
    ]

    def parse(self, response):
        # Example: extract product info
        for product in response.css('div.product'):
            yield {
                'name': product.css('h2::text').get(),
                'price': product.css('.price::text').get(),
                'url': response.urljoin(product.css('a::attr(href)').get()),
            }
        # Follow pagination links
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)