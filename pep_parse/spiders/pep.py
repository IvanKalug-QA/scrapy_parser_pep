import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse_pep(self, response):
        data = {
            'number': int(response.css(
                'h1.page-title::text').get().strip().split()[1]),
            'name': ' '.join(
                response.css(
                    'h1.page-title::text').get().strip().split()[3::]),
            'status': response.css('abbr::text').get().strip()
        }
        yield PepParseItem(data)

    def parse(self, response):
        for pep_link in response.xpath(
            '//*[@id="index-by-category"]').css(
                'td:nth-child(2) > a::attr(href)').getall():
            yield response.follow(pep_link, callback=self.parse_pep)
