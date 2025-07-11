import scrapy
import logging

class ProductSpider(scrapy.Spider):
    name = 'product_spider'
    start_urls = [
        'https://example.com/products',  # Replace with actual e-commerce URLs
        'https://example-store.com/catalog'
    ]

    def parse(self, response):
        try:
            # Example: extract product info
            for product in response.css('div.product'):
                name = product.css('h2::text').get()
                price = product.css('.price::text').get()
                url = product.css('a::attr(href)').get()
                
                if name and price:  # Only yield if we have essential data
                    yield {
                        'name': name.strip(),
                        'price': price.strip(),
                        'url': response.urljoin(url) if url else response.url,
                    }
            
            # Follow pagination links
            next_page = response.css('a.next::attr(href)').get()
            if next_page:
                yield response.follow(next_page, self.parse)
                
        except Exception as e:
            self.logger.error(f"Error parsing {response.url}: {str(e)}")
            return